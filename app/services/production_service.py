"""
Production service that generates puzzles using hashi package and stores them in database
"""

from sqlalchemy.orm import Session
from fastapi import Depends

from hashi.core import Node
from hashi.generator import generate_till_full
from hashi.solver import solve
from hashi.categorize import bucket

from app.crud.puzzle import register_puzzle_by_data, get_puzzle_count
from app.core.database import get_database
from app.services.utils import grid_to_string


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
    Retries until a solvable puzzle is produced.
    Returns (puzzle_data string, difficulty int 1-3).
    """
    while True:
      grid = generate_till_full(width, height)
      self._strip_bridges(grid)
      solutions = solve(grid, stop_at_first=True)
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


  def populate_database(self, width: int, height: int, amount: int, target_difficulty: int | None = None) -> None:
    """
    Populate database with N solvable puzzles
    If target_difficulty is None, generate random difficulty puzzles
    If target_difficulty is set (0=easy, 1=intermediate, 2=hard), generate only that difficulty
    """
    if target_difficulty is None:
      for _ in range(amount):
        self.create_puzzle(width, height)
    else:
      target_int = target_difficulty + 1  # Convert 0,1,2 to 1,2,3 (DB storage)
      saved = 0
      while saved < amount:
        puzzle_data, difficulty_int = self._generate_solvable_puzzle(width, height)
        if difficulty_int == target_int:
          register_puzzle_by_data(self.db, width, height, difficulty_int, puzzle_data)
          saved += 1


  def populate_database_till(self, width: int, height: int, amount: int, target_difficulty: int | None = None) -> None:
    """
    Keep generating puzzles until database has N puzzles of target difficulty
    If target_difficulty is None, populate all difficulties (0=easy, 1=intermediate, 2=hard)
    """
    if target_difficulty is None:
      for difficulty in [0, 1, 2]:
        self.populate_database_till(width, height, amount, difficulty)
    else:
      difficulty_int = target_difficulty + 1  # Convert 0,1,2 to 1,2,3 for DB storage
      count = get_puzzle_count(self.db, width, height, difficulty_int)
      if count < amount:
        necessary = amount - count
        self.populate_database(width, height, necessary, target_difficulty)
