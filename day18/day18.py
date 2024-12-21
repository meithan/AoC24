# Day 18: RAM Run

from collections import defaultdict
import queue
import sys
from tracemalloc import start
CLR = "\33[2K\r"

# ==============================================================================

# Get filename of input as CLI arg. If not given, default to "input.txt"
if len(sys.argv) == 1:
  input_fname = "input.txt"
else:
  input_fname = sys.argv[1]

# Read and parse input
bytes = []
with open(input_fname) as f:
  for line in f:
    bytes.append(tuple(int(x) for x in line.strip().split(",")))

if input_fname == "test1.in":
  NX, NY = 7, 7
elif input_fname == "input.txt":
  NX, NY = 71, 71

grid = []
for j in range(NY):
  grid.append([0]*NX)

def show_grid(grid):
  for line in grid:
    print("".join("#" if x == 1 else "." for x in line))

# Define the Search Nodes for this problem
neigh_offs = [(0,-1), (1,0), (0,1), (-1,0)]
class SearchNode:
  def __init__(self, x, y, parent=None):
    self.x = x
    self.y = y
    self.parent = parent
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y
  def __hash__(self):
    return hash((self.x, self.y))
  def get_neighbors(self):
    neighs = []
    for dx, dy in neigh_offs:
      nx = self.x + dx; ny = self.y + dy
      if 0 <= nx < NX and 0 <= ny < NY and grid[ny][nx] == 0:
        neigh_node = SearchNode(nx, ny, parent=self)
        cost = 1
        # neighs.append((neigh_node, cost))
        neighs.append(neigh_node)
    return neighs

# Breadth-First Search
def BFS(start_node, is_goal):

  q = queue.Queue()
  q.put(start_node)
  seen = set([start_node])

  while not q.empty():

    node = q.get()
    # print(f"{CLR}qsize={q.qsize()}, seen={len(seen)}", end="")

    if is_goal(node):
      path = [node]
      while node.parent is not None:
        path.append(node.parent)
        node = node.parent
      path = list(reversed(path))
      # print()
      return path

    neighbors = node.get_neighbors()
    for neighbor in neighbors:
      if neighbor not in seen:
        seen.add(neighbor)
        q.put(neighbor)

  # print()
  return None

# ------------------------------------------------------------------------------
# Part 1

# A-star

if input_fname == "test1.in":
  num_bytes = 12
elif input_fname == "input.txt":
  num_bytes = 1024

for i in range(num_bytes):
  x, y = bytes[i]
  grid[y][x] = 1
# show_grid(grid)

start_node = SearchNode(0, 0)
exit_node = SearchNode(NX-1, NY-1)
def heuristic(node):
  return abs(node.x - exit_node.x) + abs(node.y - exit_node.y)

# cost, path = Astar_search(start_node, lambda x: x == exit_node, heuristic)
# print(cost, path)

path = BFS(start_node, lambda x: x == exit_node)
ans1 = len(path) - 1

print("Part 1:", ans1)

# ------------------------------------------------------------------------------
# Part 2

# Reset grid
grid = []
for j in range(NY):
  grid.append([0]*NX)

for i in range(len(bytes)):
  
  x, y = bytes[i]
  grid[y][x] = 1

  path = BFS(start_node, lambda x: x == exit_node)
  print(CLR + "{} {} {}".format(i+1, bytes[i], len(path) if path is not None else "No path"), end="")
  if path is None:
    ans2 = f"{x},{y}"
    print()
    break

print("Part 2:", ans2)
