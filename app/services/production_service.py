"""
Production service that generates puzzles using hashi package and stores them in database
"""

from sqlalchemy.orm import Session
from fastapi import Depends

from hashi.generator import generate_till_full
from hashi.solver import solve
from hashi.categorize.categorize import bucket, inspect_puzzle

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

  def create_puzzle(self, width: int, height: int) -> str:
    """
    Generate a new puzzle using hashi package and register it to database
    Returns the puzzle data as a string
    """
    grid = generate_till_full(width, height)
    solve(grid)

    info = inspect_puzzle(grid)
    difficulty_str = bucket(grid, info.by_rule_steps, info.brutal_steps)
    difficulty_int = self._difficulty_to_int(difficulty_str)

    puzzle_data = grid_to_string(grid)
    register_puzzle_by_data(self.db, width, height, difficulty_int, puzzle_data)
    return puzzle_data


  def populate_database(self, width: int, height: int, amount: int, target_difficulty: int = 0) -> None:
    """
    Populate database with N solvable puzzles
    If target_difficulty is 0, generate random difficulty puzzles
    If target_difficulty is set (0=easy, 1=medium, 2=hard), generate only that difficulty
    """
    if target_difficulty == 0:
      for _ in range(amount):
        self.create_puzzle(width, height)
    else:
      for _ in range(amount):
        grid = generate_till_full(width, height)
        solve(grid)

        info = inspect_puzzle(grid)
        difficulty_str = bucket(grid, info.by_rule_steps, info.brutal_steps)
        difficulty_int = self._difficulty_to_int(difficulty_str)

        if difficulty_int == target_difficulty:
          puzzle_data = grid_to_string(grid)
          register_puzzle_by_data(self.db, width, height, difficulty_int, puzzle_data)


  def populate_database_till(self, width: int, height: int, amount: int, target_difficulty: int = 0) -> None:
    """
    Keep generating puzzles until database has N puzzles of target difficulty
    """
    if target_difficulty == 0:
      for difficulty in [1, 2, 3]:
        self.populate_database_till(width, height, amount, difficulty)
    else:
      count = get_puzzle_count(self.db, width, height, target_difficulty)
      if count < amount:
        necessary = amount - count
        self.populate_database(width, height, necessary, target_difficulty)
