# Day 11: Plutonian Pebbles

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
  stones0 = [x for x in f.readline().strip().split()]

def strip_zeros(s):
  s = s.lstrip("0")
  if s == "":
    return "0"
  else:
    return s

# Apply the rules to a single stone, return the list of new stones
def blink(stone):
  if stone == "0":
    return ["1"]
  elif len(stone) % 2 == 0:
    left = strip_zeros(stone[:len(stone)//2])
    right = strip_zeros(stone[len(stone)//2:])
    return [left, right]
  else:
    return [str(int(stone)*2024)]

# ------------------------------------------------------------------------------
# Part 1

# Just repeat the process 25 times for all stones in the list, 
stones = copy.copy(stones0)
for i in range(25):
  new_stones = []
  for stone in stones:
    new_stones += blink(stone)
  stones = new_stones
ans1 = len(stones)

print("Part 1:", ans1)

# ------------------------------------------------------------------------------
# Part 2

# For part 2, generating the list of stones is impractical
#
# We instead just count how many stones each stone will spawn, and we
# do recursively: to know how many stones there will be after N blinks
# be from a single starting stone, we blink it once, and add up how many
# spawns each of its children will create in N-1 blinks if N > 2, and
# if N = 1 we're at the base of the recursion and simply blink once and 
# use that.
#
# A crucial and necessary optimization is to memorize intermediate results:
# every time we ge the count result for (stone, num_of_blinks), we stored
# in a dict, and if that combination is ever encountered again, we just
# use the stored result and don't recurse further.

# Returns the number of spawns the given stone will generate after blinks
def count_spawns(stone, blinks):
  if blinks == 1:
    # Base case: just blink once and count
    new_stones = blink(stone)
    return len(new_stones)
  elif (stone, blinks) in memo:
    # If result is memoized, use it, don't recurse
    return memo[(stone, blinks)]
  else:
    # Blink once to get children, and add up their spawn counts(for one
    # less blink)
    new_stones = blink(stone)
    count = 0
    for new_stone in new_stones:
      count += count_spawns(new_stone, blinks-1)
    memo[(stone, blinks)] = count
    return count

memo = {}
ans2 = 0
stones = copy.copy(stones0)
for stone in stones:
  ans2 += count_spawns(stone, 75)

print("Part 2:", ans2)
