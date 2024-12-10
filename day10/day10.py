# Day 10: Hoof It

import sys
CLR = "\33[2K\r"

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
    grid.append(list((int(x) if x != "." else -1 for x in line.strip())))

nrows = len(grid)
ncols = len(grid[0])

# Finds all trails starting from the given trailhead
# Returns a dict with the summits reachable from this trailhead as keys,
# and the number of distinct trails that reach each summit as values
def find_all_trails_from(x0, y0):
  open_set = [(x0,y0)]
  trails = {}
  while len(open_set) > 0:
    # Get next place to check
    x, y = open_set.pop()
    h = grid[y][x]
    # print(x, y, h)
    if h == 9:
      # Summit reached! Record this route to this summit
      if (x,y) not in trails:
        trails[(x,y)] = 0
      trails[(x,y)] += 1
      # print(f"Summit at ({x}, {y})")
    else:
      # Loop over four neighboring places
      for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx = x + dx
        ny = y + dy
        # Ad neighboring place to open set if visitable
        # We don't check for (and exclude already visited places since
        # we want to keep all possible routes
        if 0 <= nx < ncols and 0 <= ny < nrows and grid[ny][nx] == h + 1:
          open_set.append((nx, ny))
  return trails

# ------------------------------------------------------------------------------
# Part 1

# Go over all trailheads in the map and compute the trails starting from it
# We accumulate the total scores and ratings
total_score = 0
total_rating = 0
for y in range(nrows):
  for x in range(ncols):
    if grid[y][x] == 0:
      print("Trail head ({},{})".format(x, y))
      trails = find_all_trails_from(x, y)
      trail_score = len(trails)
      trail_rating = sum(trails.values())
      print("score = {}, rating = {}".format(trail_score, trail_rating))
      total_score += trail_score
      total_rating += trail_rating

print("Part 1:", total_score)

# ------------------------------------------------------------------------------
# Part 2

print("Part 2:", total_rating)
