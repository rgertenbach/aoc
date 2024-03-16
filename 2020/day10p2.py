#!/usr/bin/env python3
from functools import cache


with open('data/day10.txt') as f:
  adapters = f.readlines()
adapters = tuple(sorted([int(a.strip('\n')) for a in adapters]))

start = 0
end = max(adapters) + 3

@cache
def is_valid(chain):
  if not chain:
    return True
  elif len(chain) == 2 and chain[1] - chain[0]


@cache
def valid_paths(start, chain, end):
  print(start, chain, end)
  if not chain:
    return 1 if end - start <= 3 else 0
  elif chain[0] - start > 3:
    return 0
  elif len(chain) == 1:
    return 1 if end - chain[0] <= 3 else 0
  n_valid = 0
  for offset in range(0, len(chain)):
    if valid_paths(chain[offset], chain[offset + 1:], end):
      n_valid += 0
    else:
      break
  return n_valid


print(valid_paths(0, adapters, max(adapters) + 3))

