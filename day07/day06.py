# Day 7: Bridge Repair

import itertools
import sys
CLR = "\33[2K\r"

# ==============================================================================

# Get filename of input as CLI arg. If not given, default to "input.txt"
if len(sys.argv) == 1:
  input_fname = "input.txt"
else:
  input_fname = sys.argv[1]

# Read and parse input
equations = []
with open(input_fname) as f:
  for line in f:
    tokens = line.strip().split(":")
    total = int(tokens[0])
    args = [int(x) for x in tokens[1].split()]
    equations.append((total, args))

# ------------------------------------------------------------------------------
# Part 1

def solvable(equation):
  total, args = equation
  for n in range(2**(len(args)-1)):
    result = args[0]
    for i in range(1,len(args)):
      if n & (2**(i-1)) == 0:
        result += args[i]
      else:
        result *= args[i]
    if result == total:
      return True
  return False

ans1 = 0
for i,equation in enumerate(equations):
  print(CLR + f"{i+1}/{len(equations)}", end="")
  if solvable(equation): 
    ans1 += equation[0]
print()

print("Part 1:", ans1)

# ------------------------------------------------------------------------------
# Part 2

def solvable2(equation):
  total, args = equation
  for combo in itertools.product(["+", "*", "||"], repeat=len(args)-1):
    result = args[0]
    for i in range(1,len(args)):
      op = combo[i-1]
      if op == "+":
        result += args[i]
      elif op == "*":
        result *= args[i]
      elif op == "||":
        result = int(str(result) + str(args[i]))
      if result > total:
        break
    if result == total:
      return True
  return False
      
ans2 = 0
for i,equation in enumerate(equations):
  print(CLR + f"{i+1}/{len(equations)}", end="")
  if solvable2(equation): 
    ans2 += equation[0]
print()

print("Part 2:", ans2)
