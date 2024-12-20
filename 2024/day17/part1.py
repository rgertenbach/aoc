import re
# 3 bit numbers (0-7) identifying 8 opcodes
# 3 registers: A, B, C holding any int
# Each instruction reads a register
# Instruction pointer identifies position of next opcode, starts at 0
# Apart from jump moves by 2 after each instruction (opcode and operand)
# If the computer tries to read an opcode past the tape it halts

with open("input.txt") as f:
  registers, program = f.read().strip("\n").split("\n\n")

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
program = [int(x) for x in program.removeprefix("Program: ").split(",")]
p = 0
out = []

while p < len(program) - 1:
  op, operand = program[p:p+2]
  if op == 0: a //= 2 ** combo(operand, a, b, c)
  elif op == 1: b ^= operand
  elif op == 2: b = combo(operand, a, b, c) % 8
  elif op == 3 and a: p = operand
  elif op == 4: b ^= c
  elif op == 5: out.append(combo(operand, a, b, c) % 8)
  elif op == 6: b = a // 2 ** combo(operand, a, b, c)
  elif op == 7: c = a // 2 ** combo(operand, a, b, c)

  if op != 3 or a == 0: p += 2
print(",".join([str(x) for x in out]))
