# Day 17: Chronospatial Computer

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
reg_A = None; reg_B = None; reg_C = None
program = []
with open(input_fname) as f:
  reg_A = int(f.readline().strip().split(":")[1])
  reg_B = int(f.readline().strip().split(":")[1])
  reg_C = int(f.readline().strip().split(":")[1])
  f.readline()
  program = [int(x) for x in f.readline().strip().split(":")[1].split(",")]
    
# ------------------------------------------------------------------------------
# Part 1

inst_set = {0: "ADV", 1: "BXL", 2: "BST", 3: "JNZ", 4: "BXC", 5: "OUT", 6: "BDV", 7: "CDV"}
def execute_program(program, registers, part2=False, debug=False):

  reg_A, reg_B, reg_C = registers

  def combo_op(operand):
    if 0 <= operand <= 3:
      return operand
    elif operand == 4:
      return reg_A
    elif operand == 5:
      return reg_B
    elif operand == 6:
      return reg_C
    elif operand == 7:
      return None
  
  if part2:
    next_i = 0

  ptr = 0
  its = 0
  output = []
  while True:

    opcode = program[ptr]
    operand = program[ptr+1]
    inst = inst_set[opcode]
    
    if debug:
      print(f"A={reg_A} B={reg_B} ({bin(reg_B)[2:]}), C={reg_C} ({bin(reg_C)[2:]})")
      print(f"ptr={ptr}, {disassemble_instruction(opcode, operand)}")

    if inst == "ADV":
      op_val = combo_op(operand)
      reg_A = int(reg_A / 2**op_val)
    
    elif inst == "BXL":
      reg_B = reg_B ^ operand
    
    elif inst == "BST":
      reg_B = combo_op(operand) % 8
    
    elif inst == "JNZ":
      if reg_A != 0:
        ptr = operand
    
    elif inst == "BXC":
      reg_B = reg_B ^ reg_C
    
    elif inst == "OUT":
      value = combo_op(operand) % 8
      output.append(value)
      if debug:
        print("output:", value)
        print(output)
      if part2:
        if value != program[next_i]:
          return False
        elif len(output) > len(program):
          return False
        else:
          next_i += 1
    
    elif inst == "BDV":
      op_val = combo_op(operand)
      reg_B = int(reg_A / 2**op_val)
    
    elif inst == "CDV":
      op_val = combo_op(operand)
      reg_C = int(reg_A / 2**op_val)

    its += 1

    if debug:
      print(f"A={reg_A} ({bin(reg_A)[2:]}), B={reg_B} ({bin(reg_B)[2:]}), C={reg_C} ({bin(reg_C)[2:]})")
      input()

    if inst != "JNZ" or reg_A == 0:
      ptr += 2
    
    if ptr > len(program)-1:
      break
  
  return output

output = execute_program(program, (reg_A, reg_B, reg_C))
ans2 = ",".join(str(x) for x in output)

print("Part 1:", ans2)

# ------------------------------------------------------------------------------
# Part 2

def combo_op_str(operand):
  if 0 <= operand <= 3:
    return str(operand)
  elif operand == 4:
    return "REG_A"
  elif operand == 5:
    return "REG_B"
  elif operand == 6:
    return "REG_C"
  elif operand == 7:
    return None

def disassemble_instruction(opcode, operand):
  inst = inst_set[opcode]
  if inst == "ADV":
    return f"REG_A = int(REG_A / 2**{combo_op_str(operand)})"
  elif inst == "BXL":
    return f"REG_B = REG_B ^ {operand}"
  elif inst == "BST":
    return f"REG_B = {combo_op_str(operand)} % 8"  
  elif inst == "JNZ":
    return f"GOTO {operand} IF REG_A != 0" 
  elif inst == "BXC":
    return f"REG_B = REG_B ^ REG_C"   
  elif inst == "OUT":
    return f"OUTPUT {combo_op_str(operand)} % 8"
  elif inst == "BDV":
    return f"REG_B = int(REG_A / 2**{combo_op_str(operand)})"    
  elif inst == "CDV":
    return f"REG_C = int(REG_A / 2**{combo_op_str(operand)})"    

def disassembler(program):
  result = []
  for i in range(len(program)//2):
    opcode = program[2*i]
    operand = program[2*i+1]
    s = disassemble_instruction(opcode, operand)
    result.append(s)
  return result

program_dis = disassembler(program)
for i,line in enumerate(program_dis):
  print(i, line)
print()

# output = execute_program(program, (reg_A, reg_B, reg_C), debug=True)

# The inputs's disassembled code is:
# 0 REG_B = REG_A % 8
# 1 REG_B = REG_B ^ 7
# 2 REG_C = int(REG_A / 2**REG_B)
# 3 REG_B = REG_B ^ 7
# 4 REG_A = int(REG_A / 2**3)
# 5 REG_B = REG_B ^ REG_C
# 6 OUTPUT REG_B % 8
# 7 GOTO 0 IF REG_A != 0
# Interpretation is as follows:
# Start with A=N, B=0, C=0
# 0: Take the 3 rightmost bits of A, store them into B
# 1: Invert B (bitwise)
# 2: Righshift A by B places (between 0 and 7), store result in C
# 3: Invert B again (restoring its value after inst 0)
# 4: Righshift A by 3 places, update A
# 5: Compute B xor C, store in B
# 6: Output 3 rightmost bits of B
# 7: Halt if A is zero, otherwise repeat
# In each iteration, output is given by:
# output = (A % 8) ^ [int(A >> inv(A % 8))] % 8
# The key insight is that the output of every iteration depends only on
# the 10 rightmost bits of A at that time, and A simply right-shifts by 3
# independently every time.
def gen_possible_A(target):
  possible = []
  for A in range(2**10):
    output = ((A % 8) ^ (int(A >> ((A % 8) ^ 7)))) % 8
    if output == target:
      possible.append(A)
  return possible

values = gen_possible_A(0)
for v in values:
  print(bin(v)[2:].zfill(10), ((v % 8) ^ (int(v >> ((v % 8) ^ 7)))) % 8, v >> 3)

# for i,target in enumerate(reversed(program)):
#   print(target)
#   values = gen_possible_A(target)
#   if i == 0:
#     possible = set(values)
#   else:
#     for v in values:
#       v 


print("Part 2:", None)
sys.exit()

# Solves the example for the program 0,3,5,4,3,0
# The example's disassembled code is:
# 0 REG_A = int(REG_A / 2**3)
# 1 OUTPUT REG_A % 8
# 2 GOTO 0 IF REG_A != 0
# That is, it takes the value of register A and repeatedly:
# (1) divides A by 8, which is equivalent to bitwise right-shifting 3 times
# (2) outputs the value corresponding to the 3 right-most bits
# This continues until the number is zero
# Hence, to reconstruct the initial value of A required to reproduce the
# program, we loop over the values of the program in reverse order, convert
# each value to its 3-bit represensetation and concatenate it. Finally, we
# add "000" at the right (because in the program division by 8 occurs before
# output)
program = [0,3,5,4,3,0]
bits = ""
for n in reversed(program):
  bits += bin(n)[2:].zfill(3)
bits += "000"
print(bits)
print(int(bits, base=2))