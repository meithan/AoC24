# Day 6: Guard Gallivant

import copy
import sys

# ==============================================================================

# Get filename of input as CLI arg. If not given, default to "input.txt"
if len(sys.argv) == 1:
  input_fname = "input.txt"
else:
  input_fname = sys.argv[1]

# Read and parse input
grid = []
with open(input_fname) as f:
  for line in f:
    grid.append([x for x in line.strip()])

ny = len(grid)
nx = len(grid[0])
for y in range(ny):
  for x in range(nx):
    if grid[y][x] == "^":
      start_x = x
      start_y = y

direcs = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
turn_right = {"up": "right", "right": "down", "down": "left", "left": "up"}

# ------------------------------------------------------------------------------
# Part 1

def guard_walk(grid):
  visited = set()
  visited2 = set()
  x, y = start_x, start_y
  direc = "up"
  while True:
    visited.add((x,y))
    visited2.add((x,y,direc))
    dx, dy = direcs[direc]
    xx = x + dx
    yy = y + dy
    if xx < 0 or xx > nx-1 or yy < 0 or yy > ny-1:
      return True, visited
    elif (xx, yy, direc) in visited2:
      return False, None
    else:
      c = grid[yy][xx]
      if c == "#":
        direc = turn_right[direc]
      else:
        x, y = xx, yy

exited, visited = guard_walk(grid)
ans1 = len(visited)

print("Part 1:", ans1)

# ------------------------------------------------------------------------------
# Part 2

ans2 = 0
for y in range(ny):
  # print(f"{y+1} / {ny}")
  for x in range(nx):
    if grid[y][x] == ".":
      new_grid = copy.deepcopy(grid)
      new_grid[y][x] = "#"
      exited, _ = guard_walk(new_grid)
      if not exited:
        ans2 += 1

print("Part 2:", ans2)
