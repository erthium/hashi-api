from fastapi import APIRouter, HTTPException, Depends
from typing import List
from random import choice

from app.services import HashiService
from app.core.settings import settings

router = APIRouter(tags=["Storage"])

@router.get(
  "/random",
  response_model=str,
  summary="Get random puzzle",
  description="Get a random puzzle",
  response_description="The puzzle data"
)
async def get_random(hashiService: HashiService = Depends(HashiService)):
  try:
    puzzle = hashiService.get_random_puzzle()
    if puzzle is None:
      raise HTTPException(status_code=404, detail="No puzzle found in the database")
    return puzzle.puzzle_data
  except Exception as e:
    raise HTTPException(status_code=500)


@router.get(
  "/{width}/{height}",
  response_model=str,
  summary="Get a random puzzle by size",
  description="Get a random puzzle by the given width and height",
  response_description="The puzzle data"
)
async def get_puzzle_by_size(width: int, height: int, hashiService: HashiService = Depends(HashiService)):
  try:
    if (width, height) not in settings.ALLOWED_GEOMETRIES:
      raise HTTPException(status_code=400, detail=f"Invalid geometry. Allowed geometries: {settings.ALLOWED_GEOMETRIES}")
    puzzle = hashiService.get_puzzle_by_size(width, height)
    if puzzle is None:
      raise HTTPException(status_code=404, detail="No puzzle found with the given geometry")
    return puzzle.puzzle_data
  except Exception as e:
    raise HTTPException(status_code=500)


@router.get(
  "/{puzzle_id}",
  response_model=str,
  summary="Get puzzle by ID",
  description="Get a puzzle by its ID",
  response_description="The puzzle data"
)
async def get_puzzle(puzzle_id: int, hashiService: HashiService = Depends(HashiService)):
  try:
    puzzle = hashiService.get_puzzle_by_id(puzzle_id)
    if puzzle is None:
      raise HTTPException(status_code=404, detail="No puzzle found with the given ID")
    return puzzle.puzzle_data
  except Exception as e:
    raise HTTPException(status_code=500)
