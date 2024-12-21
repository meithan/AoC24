# Day 19: Linen Layout

import sys
CLR = "\33[2K\r"

# ==============================================================================

# Get filename of input as CLI arg. If not given, default to "input.txt"
if len(sys.argv) == 1:
  input_fname = "input.txt"
else:
  input_fname = sys.argv[1]

# Read and parse input
with open(input_fname) as f:
  patterns = f.readline().strip().split(", ")
  f.readline()
  designs = []
  for line in f:
    designs.append(line.strip())

# print(patterns)
# print(designs)

# ------------------------------------------------------------------------------
# Part 1


def is_solvable(design, patterns):

  if design == "":
    return True

  for pat in patterns:
    if design.startswith(pat):
      solved = is_solvable(design[len(pat):], patterns)
      if solved: return True

  return False

ans1 = 0
for design in designs:
  solvable = is_solvable(design, patterns)
  # print(design, solvable)
  if solvable:
    ans1 += 1

print("Part 1:", ans1)

# ------------------------------------------------------------------------------
# Part 2

cache = {}
def count_solutions(design):

  if design == "":
    return 1

  tot_count = 0
  for pat in patterns:
    if design.startswith(pat):
      new_design = design[len(pat):]
      if new_design in cache:
        count = cache[new_design]
      else:
        count = count_solutions(new_design)
        cache[new_design] = count
      tot_count += count
      
  return tot_count

ans2 = 0
for design in designs:
  count = count_solutions(design)
  ans2 += count

print("Part 2:", ans2)
