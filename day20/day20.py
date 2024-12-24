# Day 20: Race Condition

from collections import defaultdict
import copy
import sys
from typing import DefaultDict
sys.path.append("../")
import common
CLR = "\33[2K\r"

# ==============================================================================

# Get filename of input as CLI arg. If not given, default to "input.txt"
if len(sys.argv) == 1:
  input_fname = "input.txt"
else:
  input_fname = sys.argv[1]

# Read and parse input
maze = []
with open(input_fname) as f:
  for line in f:
    maze.append(list(line.strip()))

NY = len(maze)
NX = len(maze[0])

start = None
exit = None
for j in range(NY):
  if start is not None and exit is not None:
    break
  for i in range(NX):
    if maze[j][i] == "S":
      start = (i, j)
      maze[j][i] = "."
    elif maze[j][i] == "E":
      exit = (i, j)
      maze[j][i] = "."

def show_maze(maze):
  for j in range(NY):
    print("".join(maze[j]))

RESET = common.ANSI_RESET
color_start = common.get_ansi_color("red", bright=True, bold=True)
color_exit = common.get_ansi_color("green", bright=True, bold=True)
color_path = common.get_ansi_color("cyan", bright=True, bold=True)
color_wall = common.get_ansi_color("black", bright=True)
def show_path(path):
  _path = [(node.i, node.j) for node in path]
  for j in range(NY):
    row = []
    for i in range(NX):
      row.append(RESET)
      if (i,j) == (start_node.i, start_node.j):
        row.append(color_start + "S")
      elif (i,j) == (exit_node.i, exit_node.j):
        row.append(color_exit + "E")
      elif (i,j) in _path:
        row.append(color_path + "o")
      elif maze[j][i] == "#":
        row.append(color_wall + "#")
      elif maze[j][i] == ".":
        row.append(" ")
      row.append(RESET)
    print("".join(row))

class Node:
  def __init__(self, x, y, prev=None, next=None, num=None):
    self.x = x
    self.y = y
    self.prev = prev
    self.next = next
    self.num = num
  def __hash__(self):
    return hash((self.x, self.y))
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y
  def __repr__(self):
    return f"[Node {self.num} ({self.x}, {self.y})]"

start_node = Node(start[0], start[1])
exit_node = Node(exit[0], exit[1])

# After checking it, there is a single path through the maze, so we can
# represent it as a linked list
path_orig = []
node = start_node
node.num = 0
visited = set()
neigh_offs = [(0,-1), (1,0), (0,1), (-1,0)]
while True:
  visited.add((node.x, node.y))
  path_orig.append(node)
  if node == exit_node:
    break
  for dx, dy in neigh_offs:
    nx = node.x + dx
    ny = node.y + dy
    if maze[ny][nx] == "." and (nx, ny) not in visited:
      next_node = Node(nx, ny, prev=node, num=node.num+1)
      node.next = next_node
      break
  node = next_node

# show_maze(maze)

path_dict = {(n.x, n.y): n for n in path_orig}
# for node in path_orig:
#   print("{} -> {}".format(node, node.next))

# ------------------------------------------------------------------------------
# Part 1

# Go over all internal walls and check how much they shorten the path
saved_counts = defaultdict(lambda: 0)
for j in range(1,NY-1):
  for i in range(1,NX-1):
    if maze[j][i] == "#":
      if maze[j][i-1] == "." and maze[j][i+1] == ".":
        n1 = path_dict[(i-1, j)]
        n2 = path_dict[(i+1, j)]
      elif maze[j-1][i] == "." and maze[j+1][i] == ".":
        n1 = path_dict[(i, j-1)]
        n2 = path_dict[(i, j+1)]
      else:
        # print(f"no shortcut through ({i},{j})")
        continue
      if n2.num < n1.num:
        n1, n2, = n2, n1
      saved = n2.num - n1.num - 2   # we still have to traverse the cheated wall
      # print("({},{}) saves {} ps, connects {} and {}".format(i, j, saved, n1, n2))
      # input()
      saved_counts[saved] += 1

ans1 = 0
for saved in saved_counts:
  if saved >= 100:
    ans1 += saved_counts[saved]
# print(saved_counts)

print("Part 1:", ans1)

# ------------------------------------------------------------------------------
# Part 2

def count_shortcuts(cheat_len):
  # For every node in the path before the exit node, we check which nodes
  # are accessible using a cheat of time length cheat_len (by using a flood
  # fill of that size) and whether they save time on the path
  saved_counts = defaultdict(lambda: 0)
  for k in range(len(path_orig)-1):
    node = path_orig[k]
    # print(node)
    for dy in range(-cheat_len, cheat_len+1):
      for dx in range(-cheat_len, cheat_len+1):
        d = abs(dx) + abs(dy)
        if 0 < d <= cheat_len:
          nx, ny = node.x + dx, node.y + dy
          if (nx, ny) in path_dict:
            other = path_dict[(nx, ny)]
            saved = other.num - node.num - d
            # print(saved, d, other)
            if saved > 0:
              saved_counts[saved] += 1
    # input()
  return saved_counts

saved_counts = count_shortcuts(20)

# for saved in saved_counts.items():
#   if saved >= 50:
#     print(saved_counts[saved], saved)

ans2 = 0
for saved in saved_counts:
  if saved >= 100:
    ans2 += saved_counts[saved]

print("Part 2:", ans2)
