from fastapi import APIRouter, HTTPException, Depends
from random import choice

from app.services import ProductionService
from app.schemes import PuzzleGeometry, PuzzlePopulateRequest
from app.core.settings import settings

router = APIRouter(tags=["Engine"])

puzzle_sizes: list = [(5, 5), (10, 10), (15, 15), (20, 20), (25, 25)]


@router.post(
  "/new",
  response_model=str,
  summary="Generate a new puzzle",
  description="Generates a new puzzle with the given width and height, and returns it as a string.",
  response_description="The generated puzzle."
)
async def generate(geometry: PuzzleGeometry, productionService: ProductionService = Depends(ProductionService)):
  if settings.DEVELOPMENT != 1:
    raise HTTPException(status_code=403, detail="This endpoint is only available in development mode")
  if settings.LOCK_DB_WRITE == 1:
    raise HTTPException(status_code=403, detail="Database write is locked")
  width = geometry.width
  height = geometry.height
  if not width or not height:
    raise HTTPException(status_code=400, detail="Width and height are required")
  generated_puzzle = productionService.create_puzzle(width, height)
  return generated_puzzle


@router.get(
  "/random",
  response_model=str,
  summary="Generate a random puzzle",
  description="Generates a random puzzle with a random width and height, and returns it as a string.",
  response_description="The generated puzzle."
)
async def generate_random(productionService: ProductionService = Depends(ProductionService)):
  if settings.DEVELOPMENT != 1:
    raise HTTPException(status_code=403, detail="This endpoint is only available in development mode")
  if settings.LOCK_DB_WRITE == 1:
    raise HTTPException(status_code=403, detail="Database write is locked")
  width, height = choice(puzzle_sizes)
  generated_puzzle = productionService.create_puzzle(width, height)
  return generated_puzzle


@router.post(
  "/populate",
  response_model=None,
  summary="Populate the database",
  description="Populates the database with a given amount of random puzzles with a given width and height.",
  response_description="None"
)
async def populate(data: PuzzlePopulateRequest, productionService: ProductionService = Depends(ProductionService)):
  if settings.DEVELOPMENT != 1:
    raise HTTPException(status_code=403, detail="This endpoint is only available in development mode")
  if settings.LOCK_DB_WRITE == 1:
    raise HTTPException(status_code=403, detail="Database write is locked")
  width = data.width
  height = data.height
  amount = data.amount
  target_difficulty = data.target_difficulty if data.target_difficulty else 0
  if not width or not height:
    raise HTTPException(status_code=400, detail="Width and height are required")
  if not amount:
    raise HTTPException(status_code=400, detail="Amount is required")
  productionService.populate_database(width, height, amount, target_difficulty)
  return None


@router.post(
  "/populate_till",
  response_model=None,
  summary="Populate the database till",
  description="Populates the database with a given amount of puzzles with a given width and height, until the target difficulty is reached.",
  response_description="None"
)
async def populate_till(data: PuzzlePopulateRequest, productionService: ProductionService = Depends(ProductionService)):
  if settings.DEVELOPMENT != 1:
    raise HTTPException(status_code=403, detail="This endpoint is only available in development mode")
  if settings.LOCK_DB_WRITE == 1:
    raise HTTPException(status_code=403, detail="Database write is locked")
  width = data.width
  height = data.height
  amount = data.amount
  target_difficulty = data.target_difficulty if data.target_difficulty else 0
  if not width or not height:
    raise HTTPException(status_code=400, detail="Width and height are required")
  if not amount:
    raise HTTPException(status_code=400, detail="Amount is required")
  productionService.populate_database_till(width, height, amount, target_difficulty)
  return None
