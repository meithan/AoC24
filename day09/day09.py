# Day 9: Disk Fragmenter

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
with open(input_fname) as f:
  disk = f.readline().strip()

# Expand input into blocks
blocks = []
cur_id = 0
for i,d in enumerate(disk):
    if i % 2 == 0:
      for _ in range(int(d)):
        blocks.append(cur_id)
      cur_id += 1
    else:
      for _ in range(int(d)):
        blocks.append(".")

def compute_checksum(_blocks):
  checksum = 0
  for i in range(len(_blocks)):
    if _blocks[i] != ".":
      checksum += i * _blocks[i]
  return checksum

# ------------------------------------------------------------------------------
# Part 1

# Determine indices of data and free positions
data_positions = []
free_positions = []
for i,b in enumerate(blocks):
  if b == ".":
    free_positions.append(i)
  else:
    data_positions.append(i)
num_blocks = len(blocks)
num_free = len(free_positions)
num_data = len(data_positions)

# Move data blocks from the end of the file -- stop when no move free space
# gaps are left between data
blocks1 = copy.deepcopy(blocks)
max_dest = num_data - 1
for i in range(num_free):
  k = num_data - 1 - i
  orig = data_positions[k]
  dest = free_positions[i]
  if dest > max_dest:
    break
  blocks1[dest] = blocks1[orig]
  blocks1[orig] = "."

checksum = compute_checksum(blocks1)

print("Part 1:", checksum)

# ------------------------------------------------------------------------------
# Part 2

# Determine file and free space sizes
data_blocks = []
free_blocks = []
i = 0
while i < len(blocks):
  cur = blocks[i]
  j = i
  while True:
    if j+1 > len(blocks) - 1 or blocks[j+1] != cur:
      if cur == ".":
        free_blocks.append((i, j-i+1))
      else:
        data_blocks.append((cur, i, j-i+1))
      break
    elif blocks[j+1] == cur:
      j += 1
  i = j + 1

data_blocks.sort(key=lambda x: x[0], reverse=True)

# Move all files one by one
blocks2 = copy.deepcopy(blocks)
for file_id, file_pos, file_size in data_blocks:
  # Find first free block that is big enough
  for i, (idx, free_size) in enumerate(free_blocks):
    if idx >= file_pos:
      break
    if free_size >= file_size:
      for k in range(file_size):
        blocks2[idx+k] = file_id
        blocks2[file_pos+k] = "."
      # Adjust free space
      free_blocks[i] = (idx+file_size, free_size-file_size)
      break

checksum = compute_checksum(blocks2)

print("Part 2:", checksum)

