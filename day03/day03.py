# Day 3: Mull It Over

import sys
import re

# ==============================================================================

# Get filename of input as CLI arg. If not given, default to "day<X>.in"
if len(sys.argv) == 1:
  input_fname = "input.txt"
else:
  input_fname = sys.argv[1]

# Read and parse input
memory = []
with open(input_fname) as f:
  memory = f.read().strip()

# ------------------------------------------------------------------------------
# Part 1

ans1 = 0
matches = re.findall("mul\((\d{1,3}),(\d{1,3})\)", memory)
for a,b in matches:
  ans1 += int(a) * int(b)

print("Part 1:", ans1)

# ------------------------------------------------------------------------------
# Part 2

ans2 = 0
matches = re.findall(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", memory)
enabled = True
for m in matches:
  if m == "don't()":
    enabled = False
  elif m == "do()":
    enabled = True
  else:
    if enabled:
      m1 = re.match(r"mul\((\d{1,3}),(\d{1,3})\)", m)
      ans2 += int(m1.group(1)) * int(m1.group(2))  

print("Part 2:", ans2)
