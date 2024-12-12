# Day 12: Garden Groups

import sys
CLR = "\33[2K\r"

# ==============================================================================

# Get filename of input as CLI arg. If not given, default to "input.txt"
if len(sys.argv) == 1:
  input_fname = "input.txt"
else:
  input_fname = sys.argv[1]

# Read and parse input
garden = []
with open(input_fname) as f:
  for line in f:
    garden.append(list(line.strip()))

NY = len(garden)
NX = len(garden[0])

shifts = {"L": (-1,0), "R": (1, 0), "U": (0, -1), "D": (0, 1)}

class Region:
  
  def __init__(self, letter):
    self.letter = letter
    self.squares = set()
    self.area = None
    self.perimeter = None
    self.sides = None
    self.price1 = None
    self.price2 = None
  
  def compute_price1(self):
    self.area = len(self.squares)
    self.perimeter = 0
    self.fences = set()
    for i, j in self.squares:
      for direc, (di, dj) in shifts.items():
        ni = i + di; nj = j + dj
        if ni < 0 or ni > NX-1 or nj < 0 or nj > NY-1\
        or garden[nj][ni] != self.letter:
          self.fences.add((i, j, direc))
          self.perimeter += 1
    self.price1 = self.area * self.perimeter
  
  def compute_price2(self):
    # Determine the sides of the region
    self.sides = []
    seen = set()
    for fence0 in self.fences:
      if not fence0 in seen:
        # print("starting from", fence0)
        side = set()
        open_set = [fence0]
        while len(open_set) > 0:
          fence = open_set.pop()
          side.add(fence)
          i, j, d = fence
          # Generate the two possible connecting fences
          # Two fences are connected if:
          # (1) their squares are neighbors
          # (2) their directions are the same
          if d == "U" or d == "D":
            other_fences = [(i-1, j, d), (i+1, j, d)]
          elif d == "L" or d == "R":
            other_fences = [(i, j-1, d), (i, j+1, d)]
          # If any of the two is in the set of fences, add it to open set
          # print("others:", other_fences)
          for other in other_fences:
            if other in self.fences and other not in side:
              open_set.append(other)
        self.sides.append(side)
        # print(side)
        for fence in side:
          seen.add(fence)
        # input()
    # print("sides:", len(self.sides))
    self.price2 = self.area * len(self.sides)

# ------------------------------------------------------------------------------
# Part 1

# Define array to store seen squares
seen = []
for j in range(NY):
  seen.append([False]*NX)

# Identify regions
regions = []
for j0 in range(NY):
  for i0 in range(NX):
    if not seen[j0][i0]:
      # Flood fill from this position
      open_set = [(i0, j0)]
      letter = garden[j0][i0]
      region = Region(letter)
      while len(open_set) > 0:
        i, j = open_set.pop()
        seen[j][i] = True
        region.squares.add((i, j))
        for direc, (di, dj) in shifts.items():
          ni = i + di; nj = j + dj
          if 0 <= ni < NX and 0 <= nj < NY and\
          garden[nj][ni] == letter and not seen[nj][ni]:
            if (ni, nj) not in open_set:
              open_set.append((ni, nj))
      regions.append(region)

total_price1 = 0
for region in regions:
  region.compute_price1()
  total_price1 += region.price1
  # print(region.letter, region.area, region.perimeter, region.price1)

print("Part 1:", total_price1)

# ------------------------------------------------------------------------------
# Part 2

total_price2 = 0
for region in regions:
  # print(region.letter)
  region.compute_price2()
  # print(region.price2)
  total_price2 += region.price2

print("Part 2:", total_price2)
