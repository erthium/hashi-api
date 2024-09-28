class Convertions:
  @staticmethod
  def difficulty_to_int(difficulty: str) -> int:
    """
    Convert difficulty string to integer
    """
    if difficulty == "easy":
      return 1
    if difficulty == "intermediate":
      return 2
    if difficulty == "hard":
      return 3
    return 0
  
  @staticmethod
  def difficulty_to_str(difficulty: int) -> str:
    """
    Convert difficulty integer to string
    """
    if difficulty == 1:
      return "easy"
    if difficulty == 2:
      return "intermediate"
    if difficulty == 3:
      return "hard"
    return "unknown"
