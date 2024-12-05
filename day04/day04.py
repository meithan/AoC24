# Day 4: Ceres Search 

import sys

# ==============================================================================

# Get filename of input as CLI arg. If not given, default to "day<X>.in"
if len(sys.argv) == 1:
  input_fname = "input.txt"
else:
  input_fname = sys.argv[1]

# Read and parse input
data = []
with open(input_fname) as f:
  for line in f:
    data.append(line.strip())

nrows = len(data)
ncols = len(data[0])

# ------------------------------------------------------------------------------
# Part 1

count1 = 0

# Horizontal
for line in data:
  for i in range(len(line)-3):
    if line[i:i+4] == "XMAS" or line[i:i+4] == "SAMX":
      count1 += 1

# Vertical
for c in range(ncols):
  for r in range(nrows-3):
    word = data[r][c] + data[r+1][c] + data[r+2][c] + data[r+3][c]
    if word in ["XMAS", "SAMX"]:
      count1 += 1

# Diagonal descending to the right
for c in range(ncols-3):
  for r in range(nrows-3):
    word = data[r][c] + data[r+1][c+1] + data[r+2][c+2] + data[r+3][c+3]
    if word in ["XMAS", "SAMX"]:
      count1 += 1

# Diagonal descending to the left
for c in range(3, ncols):
  for r in range(nrows-3):
    word = data[r][c] + data[r+1][c-1] + data[r+2][c-2] + data[r+3][c-3]
    if word in ["XMAS", "SAMX"]:
      count1 += 1      

print("Part 1:", count1)

# ------------------------------------------------------------------------------
# Part 2

count2 = 0

for c in range(1, ncols-1):
  for r in range(1, nrows-1):
    word1 = data[r-1][c-1] + data[r][c] + data[r+1][c+1] 
    word2 = data[r+1][c-1] + data[r][c] + data[r-1][c+1]
    if word1 in ["MAS", "SAM"] and word2 in ["MAS", "SAM"]:
      count2 += 1

print("Part 2:", count2)
