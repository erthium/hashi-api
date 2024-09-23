from pydantic import BaseModel

class PuzzleGeometry(BaseModel):
  width: int
  height: int

class PuzzlePopulateRequest(BaseModel):
  width: int
  height: int
  amount: int
