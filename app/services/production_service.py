"""
Hashi service that directly interacts with the Hashi API router and the database interactions
"""

from sqlalchemy.orm import Session
from fastapi import Depends

from app.crud.puzzle import register_puzzle_by_data, register_puzzle
from app.core.database import get_database

from app.libs.generator import generate_till_full
from app.libs.utils import grid_to_string

class ProductionService:
  def __init__(self, db: Session = Depends(get_database)):
    self.db: Session = db

  def create_puzzle(self, width: int, height: int) -> str:
    """
    Create a new puzzle
    """
    puzzle = generate_till_full(width, height)
    registered_puzzle = register_puzzle_by_data(self.db, width, height, "uncathegorised", grid_to_string(puzzle))
    return registered_puzzle.puzzle_data
  
  def populate_database(self, width: int, height: int, amount: int) -> None:
    """
    Populate the database with new puzzles
    """
    for _ in range(amount):
      print(f"Creating puzzle {_+1}/{amount}")
      puzzle_data = generate_till_full(width, height)
      register_puzzle_by_data(self.db, width, height, "uncathegorised", grid_to_string(puzzle_data))
