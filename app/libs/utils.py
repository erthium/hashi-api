from app.libs.node import Node

def grid_to_string(grid: list[list[Node]]) -> str:
  """
  Converts a grid of nodes to a string.
  """
  empty_grid: str = ""
  solution_grid: str = ""
  for line in grid:
    for node in line:
      if node.n_type == 1: 
        empty_grid += str(node.i_count)
        solution_grid += str(node.i_count)
      elif node.n_type == 0:
        empty_grid += '0'
        solution_grid += '0'
      else:
        empty_grid += '0'
        if node.b_dir == 0:
          bridge_code = -1 if node.b_thickness == 1 else -2
        elif node.b_dir == 1:
          bridge_code = -3 if node.b_thickness == 1 else -4
        solution_grid += str(bridge_code)
  return f"{len(grid)};;{len(grid[0])};;{empty_grid};;{solution_grid}"
