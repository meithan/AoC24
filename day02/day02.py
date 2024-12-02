# Day 02: Red-Nosed Reports

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

def check_safe(report):
  diffs = [report[i] - report[i-1] for i in range(1,len(report))]
  if diffs[0] > 0:
    return all([1 <= d <= 3 for d in diffs])
  elif diffs[0] < 0:
    return all([-3 <= d <= -1 for d in diffs])
  else:
    return False

count = 0
for rep in reports:
  if check_safe(rep):
    count += 1

print("Part 1:", count)

# ------------------------------------------------------------------------------
# Part 2

def check_safe2(report):
  if check_safe(report): return True
  for k in range(len(report)):
    new_rep = report[0:k] + report[k+1:]
    if check_safe(new_rep): return True
  return False

count2 = 0
for rep in reports:
  if check_safe2(rep):
    count2 += 1

print("Part 2:", count2)
