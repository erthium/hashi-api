"""
Production service for generating and registering puzzles
"""

from sqlalchemy.orm import Session
from fastapi import Depends

from app.models import Puzzle
from app.crud.puzzle import get_puzzle_by_id, get_random_puzzle
from app.core.database import get_database

class HashiService:
  def __init__(self, db: Session = Depends(get_database)):
    self.db: Session = db

  def get_random_puzzle(self) -> Puzzle:
    """
    Get a random puzzle from the database
    """
    return get_random_puzzle(self.db)


  def get_puzzle_by_id(self, puzzle_id: int) -> Puzzle:
    """
    Get a puzzle by its ID
    """
    return get_puzzle_by_id(self.db, puzzle_id)
