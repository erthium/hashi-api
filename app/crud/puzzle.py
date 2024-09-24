from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models.puzzle import Puzzle

def register_puzzle_by_data(db: Session, width: int, height: int, difficulty: int, puzzle_data: str) -> Puzzle:
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


def get_puzzle_by_id(db: Session, puzzle_id: int) -> Puzzle | None:
  """
  Get a puzzle by its ID, return the puzzle
  """
  return db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()


def get_random_puzzle(db: Session) -> Puzzle | None:
  """
  Get a random puzzle from the database
  """
  return db.query(Puzzle).order_by(func.random()).first()


def get_puzzle_by_size(db: Session, width: int, height: int) -> Puzzle | None:
  """
  Get a random puzzle by its size, return the puzzle
  """
  return db.query(Puzzle).filter(Puzzle.size_x == width, Puzzle.size_y == height).order_by(func.random()).first()


def get_puzzle_count(db: Session, width: int, height: int, difficulty: int = 0) -> int:
  """
  Get the number of puzzles in the database with the given width, height and difficulty\n
  If difficulty is set to 0 as default, it will return the count of all puzzles with the given width and height
  """
  if difficulty == 0:
    return db.query(Puzzle).filter(Puzzle.size_x == width, Puzzle.size_y == height).count()
  return db.query(Puzzle).filter(Puzzle.size_x == width, Puzzle.size_y == height, Puzzle.difficulty == difficulty).count()
