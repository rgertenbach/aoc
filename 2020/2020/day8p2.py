#!/usr/bin/env python3
from collections import defaultdict

with open('data/day8.txt') as f:
  program = f.readlines()
program = [line.strip('\n').split(' ') for line in program]
program = [(op, int(idx)) for op, idx in program]


def terminates(program):
  calls = defaultdict(int)
  pos = 0
  acc = 0
  while True:
    if calls[pos] == 1:
      return False, acc
    if pos >= len(program):
      return True, acc
    calls[pos] += 1
    op, idx = program[pos]
    if op == 'acc':
      pos += 1
      acc += idx
    elif op == 'jmp':
      pos += idx
    if op == 'nop':
      pos += 1


for i in range(len(program)):
  op, idx = program[i]
  if op == 'acc':
    continue

  new = program.copy()
  new[i] = ('jmp' if op == 'nop' else 'nop', idx)
  does_terminate, acc = terminates(new)
  if does_terminate:
    print(acc)
    break

