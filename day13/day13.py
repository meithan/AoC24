# Day 13: Claw Contraption

import re
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
  contents = f.read()
  machines = re.findall(r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)", contents)

# Each machine is a tuple (XA, YA, XB, YB, XT, YT)
for i in range(len(machines)):
  machines[i] = list(int(x) for x in machines[i])

# ------------------------------------------------------------------------------
# Part 1

# We seek integer solutions A, B to the linear system:
# A*XA + B*XB = XT
# A*YA + B*YB = YT
# The general solution to this system is:
# A = (1/D) * (YB*XT - XB*YT)
# B = (1/D) * (-YA*XT + XA*YT)
# where D is the discriminant:
# D = XA*YB - XB*YB
# If D != 0 there is a single (real) solution; if D == 0, there is no solution
# However, even if there is a solution, it could be non-integer.
# So we compute the nearest integers to the computed A and B, and check if
# they satisfy the two equations

total_cost1 = 0
for machine in machines:
  XA, YA, XB, YB, XT, YT = machine
  D = XA*YB - XB*YA
  A = int(round((YB*XT-XB*YT)/D))
  B = int(round((XA*YT-YA*XT)/D))
  solvable = A*XA + B*XB == XT and A*YA + B*YB == YT
  if solvable:
    cost = 3*A + B
    total_cost1 += cost

print("Part 1:", total_cost1)

# ------------------------------------------------------------------------------
# Part 2

total_cost2 = 0
for machine in machines:
  XA, YA, XB, YB, XT, YT = machine
  XT += 10000000000000
  YT += 10000000000000
  D = XA*YB - XB*YA
  A = int(round((YB*XT-XB*YT)/D))
  B = int(round((XA*YT-YA*XT)/D))
  solvable = A*XA + B*XB == XT and A*YA + B*YB == YT
  if solvable:
    cost = 3*A + B
    total_cost2 += cost

print("Part 2:", total_cost2)
