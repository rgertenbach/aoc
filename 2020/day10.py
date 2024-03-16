#!/usr/bin/env python3


with open('data/day10.txt') as f:
  adapters = f.readlines()
adapters = sorted([int(a.strip('\n')) for a in adapters])

last = 0
ones = 0
threes = 0
for i in range(len(adapters)):
  a = adapters[i]
  diff = a - last
  if diff == 1:
    ones += 1
  elif diff == 3:
    threes += 1
  last = a

threes += 1

print(ones * threes)
