# Day 01: 

import sys

# ==============================================================================

# Get filename of input as CLI arg. If not given, default to "day<X>.in"
if len(sys.argv) == 1:
  input_fname = sys.argv[0].replace(".py", ".in")
else:
  input_fname = sys.argv[1]

# Read and parse input
list1 = []; list2 = []
with open(input_fname) as f:
  for line in f:
    tokens = line.split()
    list1.append(int(tokens[0]))
    list2.append(int(tokens[1]))

list1.sort()
list2.sort()

# ------------------------------------------------------------------------------
# Part 1

tot_dist = 0
for a, b in zip(list1, list2):
  tot_dist += abs(a-b)

print("Part 1:", tot_dist)

# ------------------------------------------------------------------------------
# Part 2

similarity_score = 0
for a, b in zip(list1, list2):
  similarity_score += a * list2.count(a)

print("Part 2:", similarity_score)
