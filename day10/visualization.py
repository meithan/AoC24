import sys
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import scipy

# Read and parse input
grid = []
with open(sys.argv[1]) as f:
  for line in f:
    grid.append(list((int(x) if x != "." else -1 for x in line.strip())))
nrows = len(grid)
ncols = len(grid[0])
grid = np.array(grid, dtype=float)

cmap = plt.get_cmap("terrain")
colors = [cmap(x/9) for x in range(10)]
# colors[0] = "gray"
# colors[1] = "g"
# colors[9] = "r"

# Re-sample grid
zoom = 3
# grid1 = grid
# grid1 = scipy.ndimage.zoom(grid, zoom)
# grid1 = scipy.ndimage.zoom(grid, zoom, mode="grid-constant", grid_mode=True)

plt.figure(figsize=(10,10))

# Plot elevation
plt.imshow(grid, cmap="terrain", extent=(0, 1, 0, 1), vmin=0, vmax=9, interpolation="spline16", origin="lower")

# Plot contour lines
plt.contour(grid1, extent=(0, 1, 0, 1), levels=10, colors="k", alpha=0.25, linewidths=1)

# Show trailheads and summits
heads = []
summits = []
for y in range(nrows):
  for x in range(ncols):
    if grid[y][x] == 0:
      heads.append((x, y))
    elif grid[y][x] == 9:
      summits.append((x, y))
heads = np.array(heads)
offset = 0.5
xs = (heads[:,0]+offset)/ncols
ys = (heads[:,1]+offset)/nrows
plt.scatter(xs, ys, color="black", s=20)
summits = np.array(summits)
xs = (summits[:,0]+offset)/ncols
ys = (summits[:,1]+offset)/nrows
plt.scatter(xs, ys, color="red", marker="^", s=20)

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

plt.axis("off")
plt.tight_layout()

if "--save" in sys.argv:
  plt.savefig("map.png")
else:
  plt.show()