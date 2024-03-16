#!/usr/bin/env python3
from typing import Tuple

Vector = Tuple[int, int]

def hits_tree(start: Vector, vector: Vector) -> Tuple[bool, Vector]:
  x = (start[0] + vector[0]) % width
  y = start[1] + vector[1]
  return forest[y][x] == '#', (x, y)

def count_hits(forest, xy):
  print(xy)
  hits = 0
  pos = (0, 0)
  while pos[1] < len(forest) - xy[1]:
    hit, pos = hits_tree(pos, xy)
    hits += hit
  return hits

with open('data/day3.txt') as f: 
  forest = f.readlines()
width = len(forest[0]) - 1  # Stripping \r
xys = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
hits = [count_hits(forest, xy) for xy in xys]
product = 1
for factor in hits:
  product *= factor


print(product)


