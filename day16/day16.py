# Day 16: Reindeer Maze

import copy
import sys
import queue
from collections import defaultdict
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

RESET = "\u001b[0m"
# PLAYER = "\u001b[31;1m"
PLAYER = "\u001b[32;1m"
BOX = "\u001b[34;1m"
WALL = "\u001b[38;5;231m"
SPACE = "\u001b[38;5;242m"
def show_maze(maze):
  for row in maze:
    _row = ""
    for c in row:
      _row += RESET
      if c == "#":
        _row += WALL + "#"
      elif c == ".":
        _row += SPACE + "."
      elif c in "<>^v":
        _row += PLAYER + c
    print(_row)
  print(RESET)

def show_path(path):
  dir_symbols = {"N": "^", "S": "v", "E": ">", "W": "<"}
  maze1 = copy.deepcopy(maze)
  for node in path:
    maze1[node.j][node.i] = dir_symbols[node.d]
  show_maze(maze1)

neigh_offs = {"N": (0,-1), "E": (1,0), "S": (0,1), "W": (-1,0)}
neigh_dirs = {"N": ("E", "W"), "E": ("N", "S"), "S": ("E", "W"), "W": ("N", "S")}
class SearchNode:
  def __init__(self, i, j, d, parent=None):
    self.i = i
    self.j = j
    self.d = d
    self.parent = parent
  def __eq__(self, other):
    return self.i == other.i and self.j == other.j and self.d == other.d
  def __hash__(self):
    return hash((self.i, self.j, self.d))
  def __lt__(self, other):
    return True
  def __repr__(self):
    return f"<Node ({self.i}, {self.j}, {self.d})>"
  def get_neighbors(self):
    neighs = []
    for nd in neigh_dirs[self.d]:
      neighs.append((SearchNode(self.i, self.j, nd, parent=self), 1000))
    di, dj = neigh_offs[self.d]
    ni = self.i + di; nj = self.j + dj
    if 0 <= ni < NX and 0 <= nj < NY and maze[nj][ni] == ".":
      neighs.append((SearchNode(ni, nj, self.d, parent=self), 1))
    return neighs

# Does A* search from the start_node up to any node for which is_goal
# returns true
def Astar_search(start_node, is_goal, heuristic, find_all_paths=False):
  
  open_set = set()
  open_queue = queue.PriorityQueue()
  open_set.add(start_node)
  open_queue.put((0, start_node))
  gScore = defaultdict(lambda: float("inf"))
  gScore[start_node] = 0
  fScore = defaultdict(lambda: float("inf"))
  fScore[start_node] = heuristic(start_node)
  if find_all_paths:
    paths = []
    best_cost = float("inf")
  
  while not open_queue.empty():
    
    current_cost, current_node = open_queue.get()
    if not find_all_paths:
      open_set.remove(current_node)
    # print(current)
    
    if is_goal(current_node):
      path = [current_node]
      while current_node.parent is not None:
        path.append(current_node.parent)
        current_node = current_node.parent
      path = list(reversed(path))
      if find_all_paths:
        if current_cost <= best_cost:
          paths.append(path)
          best_cost = current_cost
        continue
      else:
        return current_cost, path

    neighbors = current_node.get_neighbors()
    # print(neighbors)
    # input()
    for neighbor, cost in neighbors:
      temp_gScore = gScore[current_node] + cost
      if temp_gScore <= gScore[neighbor]:
        gScore[neighbor] = temp_gScore
        fScore[neighbor] = temp_gScore + heuristic(neighbor)
        if find_all_paths or neighbor not in open_set:
          open_set.add(neighbor)
          open_queue.put((fScore[neighbor], neighbor))
  
  if find_all_paths:
    return best_cost, paths

# ------------------------------------------------------------------------------
# Part 1

start = None
end = None
for j in range(NY):
  for i in range(NX):
    if maze[j][i] == "S":
      start = (i, j)
      maze[j][i] = "."
    elif maze[j][i] == "E":
      end = (i, j)
      maze[j][i] = "."
# show_maze(maze)

start_node = SearchNode(start[0], start[1], "E")
end_nodes = [SearchNode(end[0], end[1], d) for d in neigh_dirs.keys()]
is_end_node = lambda node: node in end_nodes
heuristic = lambda node: abs(node.i-end[0]) + abs(node.j-end[1])

score, path = Astar_search(start_node, is_end_node, heuristic)
# show_path(path)

print("Part 1:", score)

# ------------------------------------------------------------------------------
# Part 2

score, paths = Astar_search(start_node, is_end_node, heuristic, find_all_paths=True)
print(len(paths), "optimal paths found")

nodes_in_best_paths = set()
for path in paths:
  # show_path(path)
  for node in path:
    nodes_in_best_paths.add((node.i, node.j))
ans2 = len(nodes_in_best_paths)

print("Part 2:", ans2)
