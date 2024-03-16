#!/usr/bin/env python3
from typing import Tuple

X = 3
Y = 1


Vector = Tuple[int, int]

def hits_tree(start: Vector, vector: Vector) -> Tuple[bool, Vector]:
  x = (start[0] + vector[0]) % width
  y = start[1] + vector[1]
  return forest[y][x] == '#', (x, y)


with open('data/day3.txt') as f: forest = f.readlines()
length = len(forest)
width = len(forest[0]) - 1 # Stripping \r

hits = 0
pos = (0, 0)
for i in range(length - Y):
  hit, pos = hits_tree(pos, (X, Y))
  hits += hit


print(hits)


