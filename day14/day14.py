# Day 14: Restroom Redoubt

from collections import defaultdict
import re
import sys
import matplotlib.pyplot as plt
import numpy as np
CLR = "\33[2K\r"

# ==============================================================================

# Get filename of input as CLI arg. If not given, default to "input.txt"
if len(sys.argv) == 1:
  input_fname = "input.txt"
else:
  input_fname = sys.argv[1]

class Robot:
  def __init__(self, x0, y0, vx, vy):
    self.x0 = int(x0)
    self.y0 = int(y0)
    self.x = self.x0
    self.y = self.y0
    self.vx = int(vx)
    self.vy = int(vy)
  def reset_pos(self):
    self.x = self.x0
    self.y = self.y0
  def __repr__(self):
    return f"<Robot p=({self.x0},{self.y0}), v=({self.vx},{self.vy})>"

# Read and parse input
robots = []
with open(input_fname) as f:
  for line in f:
    m = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line.strip())
    robots.append(Robot(*m.groups()))

NX, NY = 101, 103
# NX, NY = 11, 7

def count_robots():
  counts = defaultdict(lambda: 0)
  for r in robots:
    counts[(r.x, r.y)] += 1
  return counts

def show_robots():
  counts = count_robots()
  for j in range(NY):
    row = ""
    for i in range(NX):
      row += "." if counts[(i,j)] == 0 else str(counts[(i,j)])
    print(row)

# ------------------------------------------------------------------------------
# Part 1

def do_step():
  for r in robots:
    r.x = (r.x + r.vx) % NX
    r.y = (r.y + r.vy) % NY

for _ in range(100):
  do_step()
count_robots()

quadrant_counts = {(0,0): 0, (0,1): 0, (1,0): 0, (1,1): 0}
for r in robots:
  if r.x == NX//2 or r.y == NY//2: continue
  qx = 0 if r.x < (NX//2) else 1
  qy = 0 if r.y < (NY//2) else 1
  quadrant_counts[(qx,qy)] += 1

safety = 1
for c in quadrant_counts.values():
  safety *= c

print("Part 1:", safety)

# ------------------------------------------------------------------------------
# Part 2

# We simulate 100 steps at a time, and plot all 100 iterations in a 10x10
# grid trying to find the solution visually
for r in robots:
  r.reset_pos()
seconds = 0
while True:
  plt.figure(figsize=(12,12))
  for i in range(100):
    do_step()
    seconds += 1
    grid = np.zeros((NY,NX))
    for r in robots:
      grid[r.y][r.x] = 1
    plt.subplot(10, 10, i+1)
    plt.imshow(grid)
    plt.gca().set_axis_off()
    plt.title(seconds, fontsize=8)
  plt.tight_layout()
  plt.show()
  plt.close()

# By inspecting the first few hundred iterations, we realize that two
# special configurations with some order repeat with a fixed period: one
# where many of the robots are vertically aligned ("v"), and one where
# many are horizontally aligned ("h"). The v configuration first occurs at
# time 4 and repeats with a period of 101, hence it occurs at times
# v = 4 + 101*p for p = [0,1,...], while the h configuration first occurs at
# time 76 and has period 103, i.e. it occurs at times h = 76 + 103*q. The
# christmas tree, it would seem, occurs when the two configurations occur
# simultaneously. Hence, we must find the the smallest integers (p,q) for
# which v = h, i.e. 4 + 101*p = 76 + 103*q. Starting with p = 1, we check
# whether an integer value of q satisfies 103*q = 101*p - 72, which occurs
# when 103 divides 101*p - 72.
p = 1
while True:
  if (101*p - 72) % 103 == 0:
    ans2 = 4 + 101*p
    break
  p += 1

# Plot it
for r in robots:
  r.reset_pos()
for i in range(ans2):
  do_step()
plt.figure(figsize=(12,12))
grid = np.zeros((NY,NX))
for r in robots:
  grid[r.y][r.x] = 1
plt.imshow(grid)
plt.gca().set_axis_off()
plt.title(ans2)
plt.tight_layout()
plt.show()

print("Part 2:", ans2)
