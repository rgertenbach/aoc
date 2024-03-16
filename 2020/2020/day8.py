#!/usr/bin/env python3
from collections import defaultdict

with open('data/day8.txt') as f:
  program = f.readlines()
program = [line.strip('\n').split(' ') for line in program]
program = [(op, int(idx)) for op, idx in program]

calls = defaultdict(int)
acc = 0
pos = 0



while True:
  if calls[pos] == 1:
    break
  calls[pos] += 1
  op, idx = program[pos]
  if op == 'acc':
    acc += idx
    pos += 1
  elif op == 'jmp':
    pos += idx
  elif op == 'nop':
    pos += 1


print(acc)



