from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from random import choice

from app.services.production_service import ProductionService
from app.schemes.puzzle_requests import PuzzleGeometry, PuzzlePopulateRequest

router = APIRouter()

puzzle_sizes: list = [(5, 5), (10, 10), (15, 15), (20, 20), (25, 25)]


@router.post(
  "/new",
  response_model=str,
  summary="Generate a new puzzle",
  description="Generates a new puzzle with the given width and height, and returns it as a string.",
  response_description="The generated puzzle."
)
async def generate(geometry: PuzzleGeometry, productionService: ProductionService = Depends(ProductionService)):
  width = geometry.width
  height = geometry.height
  if not width or not height:
    raise HTTPException(status_code=400, detail="Width and height are required")
  productionService.create_puzzle(width, height)


@router.get(
  "/random",
  response_model=str,
  summary="Generate a random puzzle",
  description="Generates a random puzzle with a random width and height, and returns it as a string.",
  response_description="The generated puzzle."
)
async def generate_random(productionService: ProductionService = Depends(ProductionService)):
  width, height = choice(puzzle_sizes)
  new_puzzle = productionService.create_puzzle(width, height)
  return new_puzzle


@router.post(
  "/populate",
  response_model=None,
  summary="Populate the database",
  description="Populates the database with a given amount of random puzzles with a given width and height.",
  response_description="None"
)
async def populate(data: PuzzlePopulateRequest, productionService: ProductionService = Depends(ProductionService)):
  width = data.width
  height = data.height
  amount = data.amount
  if not width or not height:
    raise HTTPException(status_code=400, detail="Width and height are required")
  if not amount:
    raise HTTPException(status_code=400, detail="Amount is required")
  productionService.populate_database(width, height, amount)
  return None
