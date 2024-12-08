# Day 08: Resonant Collinearity

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
antennas = {}
with open(input_fname) as f:
  for line in f:
    grid.append(list(line.strip()))

nrows = len(grid)
ncols = len(grid[0])

for row in range(nrows):
  for col in range(ncols):
    c = grid[row][col]
    if c != ".":
      if c not in antennas:
        antennas[c] = []
      antennas[c].append((row,col))

# ------------------------------------------------------------------------------
# Part 1

antinodes = set()
for freq, positions in antennas.items():
  for i1 in range(len(positions)):
    for i2 in range(i1+1,len(positions)):
      y1, x1 = positions[i1]
      y2, x2 = positions[i2]
      dy = y2 - y1
      dx = x2 - x1
      an1x = x1 - dx
      an2x = x2 + dx
      an1y = y1 - dy
      an2y = y2 + dy      
      if 0 <= an1x < ncols and 0 <= an1y < nrows:
        grid[an1y][an1x] = "#"
        antinodes.add((an1x, an1y))
      if 0 <= an2x < ncols and 0 <= an2y < nrows:
        grid[an2y][an2x] = "#"
        antinodes.add((an2x, an2y))

# for row in grid:
#   print("".join(row))

ans1 = len(antinodes)

print("Part 1:", ans1)

# ------------------------------------------------------------------------------
# Part 2

antinodes2 = set()
for freq, positions in antennas.items():
  for i1 in range(len(positions)):
    for i2 in range(i1+1,len(positions)):
      y1, x1 = positions[i1]
      y2, x2 = positions[i2]
      dy = y2 - y1
      dx = x2 - x1
      m = 0
      while True:
        an1x = x1 - m*dx
        an1y = y1 - m*dy
        if an1x < 0 or an1x > ncols-1 or an1y < 0 or an1y > nrows-1:
          break
        grid[an1y][an1x] = "#"
        antinodes2.add((an1x, an1y))
        m += 1
      m = 0
      while True:
        an2x = x2 + m*dx
        an2y = y2 + m*dy
        if an2x < 0 or an2x > ncols-1 or an2y < 0 or an2y > nrows-1:
          break
        grid[an2y][an2x] = "#"
        antinodes2.add((an2x, an2y))
        m += 1        

# for row in grid:
#   print("".join(row))

ans2 = len(antinodes2)

print("Part 2:", ans2)
