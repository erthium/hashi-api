from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, UniqueConstraint
from app.core.database import Base
from datetime import datetime

class Puzzle(Base):
  __tablename__ = "puzzles"

  id = Column(Integer, primary_key=True, index=True)
  puzzle_type = Column(String, nullable=False)
  size_x = Column(Integer, nullable=False)
  size_y = Column(Integer, nullable=False)
  difficulty = Column(String, nullable=False)
  puzzle_data = Column(Text, nullable=False)
  created_at = Column(TIMESTAMP, default=datetime.now())

  # Ensures unique puzzles per size, difficulty, and data
  __table_args__ = (
    UniqueConstraint('size_x', 'size_y', 'difficulty', 'puzzle_data'),
  )
