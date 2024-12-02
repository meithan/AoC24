# Day XX: 

import sys

# ==============================================================================

# Get filename of input as CLI arg. If not given, default to "day<X>.in"
if len(sys.argv) == 1:
  input_fname = "input.txt"
else:
  input_fname = sys.argv[1]

# Read and parse input
reports = []
with open(input_fname) as f:
  for line in f:
    tokens = line.split()
    reports.append(list(int(x) for x in tokens))

# ------------------------------------------------------------------------------
# Part 1

print("Part 1:", None)

# ------------------------------------------------------------------------------
# Part 2

print("Part 2:", None)
