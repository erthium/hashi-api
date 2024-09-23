## If the island count average is closer to 3 or 4, the puzzle is more difficult
ISLAND_WEIGHT_FACTOR: float = 0.59
## If the island count is higher, the puzzle is more difficult
ISLAND_AMOUNT_FACTOR: float = 0.18
## If there is a high amount of 7 or 8 islands, the puzzle is easier
ABOVE_SIX_FACTOR: float = 0.23

EASY_THRESHOLD: float = 0.2
MEDIUM_THRESHOLD: float = 0.4
HARD_THRESHOLD: float = 1.0 # unnecessary, but for clarity
