from fastapi import APIRouter, HTTPException, Request
from typing import List
from random import choice

from app.libs.generator import generate_till_full
from app.libs.utils import grid_to_string

router = APIRouter()

puzzle_sizes: list = [(5, 5), (10, 10), (15, 15), (20, 20), (25, 25)]

@router.post(
  "/new",
  response_model=str,
  summary="Generate a new puzzle",
  description="Generates a new puzzle with the given width and height, and returns it as a string.",
  response_description="The generated puzzle."
)
async def calculate(width: int, height: int):
  if not width or not height:
    raise HTTPException(status_code=400, detail="Width and height are required")
  new_puzzle = generate_till_full(width, height)
  return grid_to_string(new_puzzle)


@router.get(
  "/random",
  response_model=str,
  summary="Generate a random puzzle",
  description="Generates a random puzzle with a random width and height, and returns it as a string.",
  response_description="The generated puzzle."
)
async def random():
  width, height = choice(puzzle_sizes)
  new_puzzle = generate_till_full(width, height)
  return grid_to_string(new_puzzle)
