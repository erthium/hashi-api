"""Utility functions for services"""

def grid_to_string(grid) -> str:
  """
  Converts a hashi Node grid to string format.
  Format: width;;height;;empty_grid;;solution_grid
  """
  from hashi.core import Node

  empty_grid: str = ""
  solution_grid: str = ""

  for line in grid:
    for node in line:
      # n_type: 0=empty, 1=island, 2=bridge
      if node.n_type == 1:
        # Island node
        empty_grid += str(node.i_count)
        solution_grid += str(node.i_count)
      elif node.n_type == 0:
        # Empty node
        empty_grid += '0'
        solution_grid += '0'
      else:
        # Bridge node (n_type == 2)
        empty_grid += '0'
        if node.b_dir == 0:  # horizontal
          bridge_code = -1 if node.b_thickness == 1 else -2
        elif node.b_dir == 1:  # vertical
          bridge_code = -3 if node.b_thickness == 1 else -4
        else:
          bridge_code = 0
        solution_grid += str(bridge_code)

  return f"{len(grid)};;{len(grid[0])};;{empty_grid};;{solution_grid}"
