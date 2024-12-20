import re

with open("input.txt") as f:
  registers, sprogram = f.read().strip("\n").split("\n\n")

def combo(x, a, b, c):
  if x == 7: raise RuntimeError("7 is an Invalid opcode")
  if x == 4: return a
  if x == 5: return b
  if x == 6: return c
  return x


a, b, c = [
    int(re.findall(r"Register \w: (.*)", r)[0])
    for r in registers.split("\n")
]
fprogram = sprogram.removeprefix("Program: ")
program = [int(x) for x in fprogram.split(",")]

def format(xs): return ",".join([str(x) for x in xs])
longest_match = 0

def run(a, b, c) -> bool:
  global longest_match
  orig_a = a
  p = 0
  out = []
  while p < len(program) - 1:
    op, operand = program[p:p+2]
    if op == 0: a //= 2 ** combo(operand, a, b, c)
    elif op == 1: b ^= operand
    elif op == 2: b = combo(operand, a, b, c) % 8
    elif op == 3 and a: p = operand
    elif op == 4: b ^= c
    elif op == 5:
      out.append(combo(operand, a, b, c) % 8)
      if fprogram == format(out): return True
      if not fprogram.startswith(format(out)): return False
      if len(out) > 14:
        print(f"Match {len(out)} with {orig_a}: {orig_a%(2**(3 * 12)):b}")

    elif op == 6: b = a // 2 ** combo(operand, a, b, c)
    elif op == 7: c = a // 2 ** combo(operand, a, b, c)

    if op != 3 or a == 0: p += 2
  return fprogram == format(out)


#     28343889597
#         1223973 too low
# 164278899142333
# 732096929558205  too high
# x = 0
# 31_700_000_000
# Match 9 with 695037885: 111_110_111_101 shift 12, 
a = 0
# this was done iteratively
print(f"match needed {len(program)}")
while not run((a << 36) + 0b100_100_101_001_011_011_010_110_111_010_111_101, b, c):
  # suffix = int("100111100110110101", 2)
  # x += 1
  # a = int(f"{x:b}{suffix:b}", 2)
  if a % 100_000_000 == 0:
    print(a)
  a += 1
print(f"Solution: {(a << 36) + 0b100_100_101_001_011_011_010_110_111_010_111_101}")
