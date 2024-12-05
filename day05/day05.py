# Day 5: Print Queue

import sys

# ==============================================================================

# Get filename of input as CLI arg. If not given, default to "input.txt"
if len(sys.argv) == 1:
  input_fname = "input.txt"
else:
  input_fname = sys.argv[1]

# Read and parse input
rules = set()
updates = []
with open(input_fname) as f:
  for line in f:
    if "|" in line:
      tokens = line.strip().split("|")
      rules.add((int(tokens[0]), int(tokens[1])))
    elif line != "\n":
      tokens = line.strip().split(",")
      updates.append(list(int(x) for x in tokens))

# ------------------------------------------------------------------------------
# Part 1

def is_correct(update):
  for a, b in rules:
    if a in update and b in update:
      if update.index(a) > update.index(b):
        return False
  return True

bad_ones = []
ans1 = 0
for update in updates:
  if is_correct(update):
    ans1 += update[len(update)//2]
  else:
    bad_ones.append(update)

print("Part 1:", ans1)

# ------------------------------------------------------------------------------
# Part 2

def fix(update):
  while True:
    done = True
    for a, b in rules:
      if a in update and b in update:
        i = update.index(a)
        j = update.index(b)
        if i > j:
          update[i] = b
          update[j] = a
          done = False
          break
    if done: return

ans2 = 0
for update in bad_ones:
  fix(update)
  ans2 += update[len(update)//2]

print("Part 2:", ans2)
