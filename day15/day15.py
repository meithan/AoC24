# Day 15: Warehouse Woes

import copy
import sys
CLR = "\33[2K\r"

# ==============================================================================

# Get filename of input as CLI arg. If not given, default to "input.txt"
if len(sys.argv) == 1:
  input_fname = "input.txt"
else:
  input_fname = sys.argv[1]

# Read and parse input
grid = []
moves = ""
with open(input_fname) as f:
  for line in f:
    if line == "\n":
      break
    grid.append(list(line.strip()))
  for line in f:
    moves += line.strip()

grid_orig = copy.deepcopy(grid)
NY = len(grid)
NX = len(grid[0])

shifts = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}

def find_robot():
  for j in range(NY):
    for i in range(NX):
      if grid[j][i] == "@":
        return i, j

# Checks whether the entity (robot or box) at (x,y) can move in that direction
# This is a recursive check, checking all objects in the line 
def can_move(x, y, move):
  dx, dy = shifts[move]
  newx = x + dx
  newy = y + dy
  next_obj = grid[newy][newx]
  if next_obj == "#":
    return False
  elif next_obj == ".":
    return True
  elif next_obj == "O":
    return can_move(newx, newy, move)
  elif next_obj in "[]":
    if move in "<>":
      return can_move(newx, newy, move)
    elif move in "^v":
      if next_obj == "[":
        return can_move(newx, newy, move) and can_move(newx+1, newy, move)
      elif next_obj == "]":
        return can_move(newx, newy, move) and can_move(newx-1, newy, move)

# Moves object from x,y towards 'move' (it is assumed to be valid)
# This moves all objects in the line recursively
def do_move(x, y, move):
  obj = grid[y][x]
  grid[y][x] = "."
  dx, dy = shifts[move]
  newx = x + dx; newy = y + dy
  next_obj = grid[newy][newx]
  if next_obj == ".":
    grid[newy][newx] = obj
    return
  elif next_obj == "O":
    do_move(newx, newy, move)
    grid[newy][newx] = obj
    return
  elif next_obj in "[]":
    if move in "<>":
      do_move(newx, newy, move)
      grid[newy][newx] = obj
      return
    elif move in "^v":
      if next_obj == "[":
        do_move(newx, newy, move)
        do_move(newx+1, newy, move)
      elif next_obj == "]":
        do_move(newx, newy, move)
        do_move(newx-1, newy, move)
      grid[newy][newx] = obj

# Shows the grind with fancy pants ANSI color sequences
RESET = "\u001b[0m"
ROBOT = "\u001b[31;1m"
BOX = "\u001b[34;1m"
WALL = "\u001b[38;5;231m"
SPACE = "\u001b[38;5;242m"
def show_grid():
  for j in range(NY):
    row = ""
    for i in range(NX):
      row += RESET
      if grid[j][i] == "@":
        row += ROBOT + "@"
      elif grid[j][i] in ["O", "[", "]"]:
        row += BOX + grid[j][i]
      elif grid[j][i] == "#":
        row += WALL + "#"
      elif grid[j][i] == ".":
        row += SPACE + "."
    row += RESET
    print(row)

# ------------------------------------------------------------------------------
# Part 1

# Find the robot and execute its list of moves
# show_grid()
robot_x, robot_y = find_robot()
for move in moves:
  # if can_move(rob_x, rob_y, move): print("Moving", move)
  # else: print("Can't", move)
  if can_move(robot_x, robot_y, move):
    do_move(robot_x, robot_y, move)
    dx, dy = shifts[move]
    robot_x += dx; robot_y += dy  
#   show_grid()
#   input()
# show_grid()

# Sum of GPS coordinates
ans1 = 0
for j in range(NY):
  for i in range(NX):
    if grid[j][i] == "O":
      ans1 += 100*j + i

print("Part 1:", ans1)

# ------------------------------------------------------------------------------
# Part 2

# Augment grid
grid1 = copy.deepcopy(grid_orig)
grid = []
for row in grid1:
  new_row = ""
  for c in row:
    if c == "#":
      new_row += "##"
    elif c == "O":
      new_row += "[]"
    elif c == ".":
      new_row += ".."
    elif c == "@":
      new_row += "@."
  grid.append(list(new_row))
NY = len(grid)
NX = len(grid[0])
# show_grid()

robot_x, robot_y = find_robot()

# Execute moves in augmented grid
for move in moves:
  # input()
  # if can_move(robot.x, robot.y, move): print("Moved", move)
  # else: print("Couldn't", move)
  if can_move(robot_x, robot_y, move):
    do_move(robot_x, robot_y, move)
    dx, dy = shifts[move]
    robot_x += dx; robot_y += dy  
  # show_grid()

# show_grid()

# Compute sum of GPS coordinates
ans2 = 0
for j in range(NY):
  for i in range(NX):
    if grid[j][i] == "[":
      ans2 += 100*j + i

print("Part 2:", ans2)
 