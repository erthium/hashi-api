from dataclasses import dataclass
from node import Node

from difficulty_map import ISLAND_WEIGHT_FACTOR, ISLAND_AMOUNT_FACTOR, ABOVE_SIX_FACTOR, EASY_THRESHOLD, MEDIUM_THRESHOLD

@dataclass
class PuzzleInformation:
    island_amount: int
    total_island_count: int
    total_seven_count: int
    total_eight_count: int
    min_island_count: int
    max_island_count: int


def get_island_amount_boundries(width: int, height: int) -> list[int, int]:
    """
    Gets a geometry and returns the island amount boundries.\n
    Returns a list of two integers, min and max.\n
    Returns [-1, -1] if geometry is not found in map.
    """
    min_count: int = 2
    max_count: int = width * height / 3
    return [min_count, max_count]


def inspect_puzzle(grid: list[list[Node]]) -> PuzzleInformation:
    grid_width: int = len(grid)
    grid_height: int = len(grid[0])
    island_amount: int = 0 # amount of islands
    total_island_count: int = 0 # sum of all island counts
    total_seven_count: int = 0
    total_eight_count: int = 0
    for x in range(grid_width):
        for y in range(grid_height):
            if grid[x][y].n_type == 1:
                island_amount += 1
                total_island_count += grid[x][y].i_count
                if grid[x][y].i_count == 7:
                    total_seven_count += 1
                if grid[x][y].i_count == 8:
                    total_eight_count += 1
    min_count, max_count = get_island_amount_boundries(grid_width, grid_height)
    return PuzzleInformation(island_amount, total_island_count, total_seven_count, total_eight_count, min_count, max_count)


def determine_difficulty(grid: list[list[Node]]) -> float:
    """
    Gets a grid and returns a difficulty rating.\n
    Rating is an float between 0 and 1.
    """
    info: PuzzleInformation = inspect_puzzle(grid)
    island_weigth = info.total_island_count / info.island_amount / 8
    island_amount_weight = (info.island_amount - info.min_island_count) / (info.max_island_count - info.min_island_count)
    above_six_weight = (info.total_seven_count + info.total_eight_count) / info.island_amount
    difficulty = island_weigth * ISLAND_WEIGHT_FACTOR + island_amount_weight * ISLAND_AMOUNT_FACTOR + above_six_weight * ABOVE_SIX_FACTOR
    return difficulty
