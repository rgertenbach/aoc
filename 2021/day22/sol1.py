#!/usr/bin/python3

import itertools
import sys
from cuboid import Cuboid, Instruction, State
from reactor import Reactor

# Solve this by using a "cube set"
# Represent cubes in the terms of pure subcubes


def read_instructions(filename):
  with open(filename) as f:
    lines = f.readlines()
  return [Instruction.parse(line) for line in lines]


instructions = read_instructions(sys.argv[1])
new = instructions[0].cuboid + instructions[1].cuboid
r = Reactor()
for instruction in instructions:
  if min(instruction.cuboid.as_tuple()) >= -50 and max(instruction.cuboid.as_tuple()) <= 50:
    if instruction.state == State.ON:
      r = r + instruction.cuboid
    else:
      r = r - instruction.cuboid

print(len(r))



