"""
Hashi service that directly interacts with the Hashi API router and the database interactions
"""

from sqlalchemy.orm import Session
from fastapi import Depends

from app.crud.puzzle import register_puzzle_by_data, get_puzzle_count
from app.core.database import get_database

from app.libs.generator import generate_till_full
from app.libs.cathegorise import get_difficulty
from app.libs.utils import grid_to_string


class ProductionService:
  def __init__(self, db: Session = Depends(get_database)):
    self.db: Session = db


  def create_puzzle(self, width: int, height: int) -> str:
    """
    Create a new puzzle and register it to the database\n
    Return the puzzle data as a string
    """
    puzzle = generate_till_full(width, height)
    difficulty = get_difficulty(puzzle)
    puzzle_data = grid_to_string(puzzle)
    register_puzzle_by_data(self.db, width, height, difficulty, puzzle_data)
    return puzzle_data


  def populate_database(self, width: int, height: int, amount: int, target_difficulty: int = 0) -> None:
    """
    Populate the database with new puzzles\n
    If target_difficulty is 0 as default, puzzles will be generated randomly\n
    1 for easy, 2 for medium, 3 for hard\n
    If target_difficulty is set, puzzles will be generated with the specific difficulty
    """
    if target_difficulty == 0:
      for _ in range(amount):
        #print(f"Creating puzzle {_+1}/{amount}")
        puzzle_data = generate_till_full(width, height)
        difficulty = get_difficulty(puzzle_data)
        register_puzzle_by_data(self.db, width, height, difficulty, grid_to_string(puzzle_data))
    else:
      for _ in range(amount):
        #print(f"Creating puzzle {_+1}/{amount}")
        puzzle_data = generate_till_full(width, height)
        difficulty = get_difficulty(puzzle_data)
        while difficulty != target_difficulty:
          puzzle_data = generate_till_full(width, height)
          difficulty = get_difficulty(puzzle_data)
        register_puzzle_by_data(self.db, width, height, difficulty, grid_to_string(puzzle_data))


  def populate_database_till(self, width: int, height: int, amount: int, target_difficulty: int = 0) -> None:
    if target_difficulty == 0:
      print("Populating all difficulties")
      for difficulty in [1, 2, 3]:
        self.populate_database_till(width, height, amount, difficulty)
    else:
      print(f"Populating with target difficulty {target_difficulty}")
      count = get_puzzle_count(self.db, width, height, target_difficulty)
      if count >= amount:
        print(f"Database already has {count} puzzles with the target difficulty")
        return
      necessary_amount = amount - count
      self.populate_database(width, height, necessary_amount, target_difficulty)
      print(f"Database now has {amount} puzzles with the target difficulty")
