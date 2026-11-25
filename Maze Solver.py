from collections import deque
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np



MAZE = [
    [2, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
]


def find_positions(grid):
  start = goal = None
  for r, row in enumerate(grid):
    for c, val in enumerate(row):
      if val == 2:
        start = (r, c)
      elif val == 3:
        goal = (r, c)
  return start, goal


def get_neighbors(grid, pos):
  rows, cols = len(grid), len(grid[0])
  r, c = pos
  # Up, Right, Down, Left
  directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
  neighbors = []
  for dr, dc in directions:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
      neighbors.append((nr, nc))
  return neighbors


def reconstruct_path(parent, start, goal):
  if goal not in parent and start != goal:
    return []
  path = []
  curr = goal
  while curr is not None:
    path.append(curr)
    curr = parent.get(curr)
  path.reverse()
  return path


def solve_bfs(grid, start, goal):
  queue = deque([start])
  visited = {start}
  parent = {start: None}
  visit_order = []

  while queue:
    curr = queue.popleft()
    visit_order.append(curr)
    if curr == goal:
      break
    for nxt in get_neighbors(grid, curr):
      if nxt not in visited:
        visited.add(nxt)
        parent[nxt] = curr
        queue.append(nxt)

  path = reconstruct_path(parent, start, goal)
  return visit_order, path


def solve_dfs(grid, start, goal):
  stack = [start]
  visited = {start}
  parent = {start: None}
  visit_order = []

  while stack:
    curr = stack.pop()
    visit_order.append(curr)
    if curr == goal:
      break
    # Reverse neighbors so top of stack explores in natural order
    for nxt in reversed(get_neighbors(grid, curr)):
      if nxt not in visited:
        visited.add(nxt)
        parent[nxt] = curr
        stack.append(nxt)

  path = reconstruct_path(parent, start, goal)
  return visit_order, path


def animate_solver(grid, start, goal, visit_order, path, title):
  rows, cols = len(grid), len(grid[0])
  base_grid = np.array(grid, dtype=float)

  
  display_grid = np.ones((rows, cols))
  display_grid[base_grid == 1] = 0

  cmap = plt.cm.colors.ListedColormap(
      ["#1e293b", "#f8fafc", "#93c5fd", "#f59e0b", "#22c55e", "#ef4444"]
  )
  bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
  norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

  fig, ax = plt.subplots(figsize=(6, 6))
  img = ax.imshow(display_grid, cmap=cmap, norm=norm)
  ax.set_title(title)
  ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
  ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
  ax.grid(which="minor", color="#cbd5e1", linestyle="-", linewidth=1)
  ax.tick_params(
      which="both", bottom=False, left=False, labelbottom=False, labelleft=False
  )

  
  frames = []
  current_visited = set()
  for cell in visit_order:
    current_visited.add(cell)
    frames.append(("visit", set(current_visited), []))

  current_path = []
  for cell in path:
    current_path.append(cell)
    frames.append(("path", set(current_visited), list(current_path)))

  def update(frame_data):
    _, vis, pth = frame_data
    g = np.ones((rows, cols))
    g[base_grid == 1] = 0
    for r, c in vis:
      g[r, c] = 2
    for r, c in pth:
      g[r, c] = 3
    g[start] = 4
    g[goal] = 5
    img.set_data(g)
    return [img]

  ani = FuncAnimation(
      fig, update, frames=frames, interval=80, repeat=False, blit=True
  )
  plt.tight_layout()
  plt.show()


if __name__ == "__main__":
  start_pos, goal_pos = find_positions(MAZE)

  bfs_visited, bfs_path = solve_bfs(MAZE, start_pos, goal_pos)
  print(f"BFS -> Visited: {len(bfs_visited)} cells | Path length: {len(bfs_path)}")
  animate_solver(
      MAZE,
      start_pos,
      goal_pos,
      bfs_visited,
      bfs_path,
      f"BFS (Shortest Path: {len(bfs_path)} steps)",
  )

  dfs_visited, dfs_path = solve_dfs(MAZE, start_pos, goal_pos)
  print(f"DFS -> Visited: {len(dfs_visited)} cells | Path length: {len(dfs_path)}")
  animate_solver(
      MAZE,
      start_pos,
      goal_pos,
      dfs_visited,
      dfs_path,
      f"DFS (Found Path: {len(dfs_path)} steps)",
  )