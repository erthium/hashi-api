from sqlalchemy.orm import Session
from app.models.puzzle import Puzzle
from sqlalchemy.sql import func

def register_puzzle_by_data(db: Session, width: int, height: int, difficulty: str, puzzle_data: str) -> Puzzle:
  """
  Register a new puzzle to the database, commit, and return the puzzle
  """
  db_puzzle = Puzzle(
    puzzle_type="hashi",
    size_x=width,
    size_y=height,
    difficulty=difficulty,
    puzzle_data=puzzle_data
  )
  db.add(db_puzzle)
  db.commit()
  db.refresh(db_puzzle)
  return db_puzzle

def register_puzzle(db: Session, puzzle: Puzzle) -> Puzzle:
  """
  Register a new puzzle to the database, commit, and return the puzzle
  """
  db.add(puzzle)
  db.commit()
  db.refresh(puzzle)
  return puzzle


def get_puzzle_by_id(db: Session, puzzle_id: int):
  """
  Get a puzzle by its ID, return the puzzle
  """
  return db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()


def get_random_puzzle(db: Session):
  """
  Get a random puzzle from the database
  """
  return db.query(Puzzle).order_by(func.random()).first()
