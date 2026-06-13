"""
Production service that generates puzzles using hashi package and stores them in database
"""

import logging
import time

from sqlalchemy.orm import Session
from fastapi import Depends

from hashi.core import Node
from hashi.generator import generate_till_full
from hashi.solver import solve
from hashi.categorize import bucket

from app.crud.puzzle import register_puzzle_by_data, get_puzzle_count
from app.core.database import get_database
from app.services.utils import grid_to_string

logger = logging.getLogger(__name__)

_DIFFICULTY_NAMES = {1: "easy", 2: "intermediate", 3: "hard"}

# The hashi solver has no built-in cap on brute-force search — solve_brutally()
# is an unbounded recursive DFS. A pathological puzzle can search effectively
# forever. We cap it via the progress_callback: once brutal_steps exceeds this
# limit we raise, abort the solve, and discard the puzzle (regenerate instead).
# Most puzzles solve by rules alone (brutal_steps == 0), so this only trips on
# the rare adversarial board. Tune higher to allow genuinely harder puzzles.
BRUTAL_STEP_CAP = 50000


class _StepCapExceeded(Exception):
  """Raised from the solver progress callback when brutal_steps exceeds the cap."""


def _make_cap_callback(cap: int):
  """Build a solver progress_callback that aborts once brutal_steps > cap."""
  def _callback(rule_steps: int, brutal_steps: int) -> None:
    if brutal_steps > cap:
      raise _StepCapExceeded(brutal_steps)
  return _callback


class ProductionService:
  def __init__(self, db: Session = Depends(get_database)):
    self.db: Session = db

  @staticmethod
  def _difficulty_to_int(difficulty_str: str) -> int:
    """Map hashi difficulty string to int: easy=1, intermediate=2, hard=3"""
    mapping = {'easy': 1, 'intermediate': 2, 'hard': 3}
    return mapping.get(difficulty_str, 1)

  @staticmethod
  def _strip_bridges(grid: list[list[Node]]) -> None:
    """
    Remove construction bridges and reset island current_in.
    generate_till_full leaves bridges in place, but solve() expects an empty board.
    """
    for row in grid:
      for node in row:
        if node.n_type == 2:
          node.make_empty()
        elif node.n_type == 1:
          node.current_in = 0

  def _generate_solvable_puzzle(self, width: int, height: int) -> tuple[str, int]:
    """
    Generate a puzzle and solve it to determine difficulty.
    Retries until a solvable puzzle is produced (discarding unsolvable boards and
    ones whose brute-force search exceeds BRUTAL_STEP_CAP).
    Returns (puzzle_data string, difficulty int 1-3).
    """
    cap_callback = _make_cap_callback(BRUTAL_STEP_CAP)
    while True:
      grid = generate_till_full(width, height)
      self._strip_bridges(grid)
      try:
        solutions = solve(grid, stop_at_first=True, progress_callback=cap_callback)
      except _StepCapExceeded:
        continue  # too hard to brute-force, discard and retry
      if not solutions:
        continue  # unsolvable, discard and retry

      solution = solutions[0]
      difficulty_str = bucket(grid, solution.rule_steps, solution.brutal_steps)
      difficulty_int = self._difficulty_to_int(difficulty_str)
      puzzle_data = grid_to_string(solution.grid)
      return puzzle_data, difficulty_int

  def create_puzzle(self, width: int, height: int) -> str:
    """
    Generate a new solvable puzzle using hashi package and register it to database
    Returns the puzzle data as a string
    """
    puzzle_data, difficulty_int = self._generate_solvable_puzzle(width, height)
    register_puzzle_by_data(self.db, width, height, difficulty_int, puzzle_data)
    return puzzle_data


  def _generate_into_buckets(self, width: int, height: int, targets: dict[int, int]) -> None:
    """
    Single generation loop that buckets each puzzle by its difficulty.
    `targets` maps difficulty int (1=easy, 2=intermediate, 3=hard) -> how many to save.
    Every generated puzzle is saved into its difficulty bucket if that bucket still
    needs more; otherwise it is discarded. Loops until every bucket is satisfied — so
    once the common difficulties fill up, generation continues only to fill the rarer
    ones (still capturing the rare difficulty whenever it shows up, never wasting it).
    """
    targets = {d: n for d, n in targets.items() if n > 0}
    if not targets:
      logger.info("populate: nothing to do (all targets already satisfied)")
      return

    start = time.perf_counter()
    wanted = ", ".join(f"{_DIFFICULTY_NAMES[d]}={n}" for d, n in sorted(targets.items()))
    logger.info("populate: %dx%d, want %s — single bucketed loop", width, height, wanted)

    saved = {d: 0 for d in targets}
    discarded = {1: 0, 2: 0, 3: 0}
    generated = 0
    while any(saved[d] < n for d, n in targets.items()):
      puzzle_data, difficulty_int = self._generate_solvable_puzzle(width, height)
      generated += 1
      if difficulty_int in targets and saved[difficulty_int] < targets[difficulty_int]:
        register_puzzle_by_data(self.db, width, height, difficulty_int, puzzle_data)
        saved[difficulty_int] += 1
        logger.info(
          "populate: saved %s %d/%d (generated %d; saved easy=%d inter=%d hard=%d; "
          "discarded easy=%d inter=%d hard=%d)",
          _DIFFICULTY_NAMES[difficulty_int], saved[difficulty_int], targets[difficulty_int],
          generated, saved.get(1, 0), saved.get(2, 0), saved.get(3, 0),
          discarded[1], discarded[2], discarded[3],
        )
      else:
        discarded[difficulty_int] += 1

    total_saved = sum(saved.values())
    elapsed = time.perf_counter() - start
    logger.info(
      "populate: DONE %d puzzles in %.1fs — generated %d total "
      "(%.1f generated per saved; discarded easy=%d inter=%d hard=%d)",
      total_saved, elapsed, generated, generated / max(total_saved, 1),
      discarded[1], discarded[2], discarded[3],
    )

  def populate_database(self, width: int, height: int, amount: int, target_difficulty: int | None = None) -> None:
    """
    Populate database with solvable puzzles
    If target_difficulty is None, generate `amount` puzzles of EACH difficulty (easy, intermediate, hard)
    If target_difficulty is set (0=easy, 1=intermediate, 2=hard), generate `amount` of only that difficulty
    """
    if target_difficulty is None:
      targets = {1: amount, 2: amount, 3: amount}
    else:
      targets = {target_difficulty + 1: amount}  # Convert 0,1,2 to 1,2,3 (DB storage)
    self._generate_into_buckets(width, height, targets)

  def populate_database_till(self, width: int, height: int, amount: int, target_difficulty: int | None = None) -> None:
    """
    Keep generating until the database has `amount` puzzles of the target difficulty.
    If target_difficulty is None, top up ALL difficulties to `amount` each.
    Only the shortfall per difficulty is generated (a single bucketed loop fills them together).
    """
    if target_difficulty is None:
      difficulties = [1, 2, 3]
    else:
      difficulties = [target_difficulty + 1]  # Convert 0,1,2 to 1,2,3 (DB storage)

    targets = {}
    for difficulty_int in difficulties:
      count = get_puzzle_count(self.db, width, height, difficulty_int)
      shortfall = max(0, amount - count)
      logger.info(
        "populate_till: difficulty=%s has %d/%d in DB — need %d more",
        _DIFFICULTY_NAMES[difficulty_int], count, amount, shortfall,
      )
      targets[difficulty_int] = shortfall

    self._generate_into_buckets(width, height, targets)
