from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from random import choice

from app.libs.generator import generate_till_full
from app.libs.utils import grid_to_string
from app.services.hashi_service import HashiService

router = APIRouter()

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
    return puzzle.puzzle_data
  except Exception as e:
    raise HTTPException(status_code=500)
