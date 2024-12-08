from collections import defaultdict
import itertools
import math

with open("input.txt") as f:
  ant = f.read().strip("\n").split("\n")

rows = len(ant)
cols = len(ant[0])
antennas = defaultdict(list)


def antinodes(a1, a2) -> set[tuple[int, int]]:
  if a1[0] == a2[0]: return {(a1[0], c) for c in range(cols)}
  if a1[1] == a2[1]: return {(r, a1[1]) for r in range(cols)}
  dy = a2[0] - a1[0]
  dx = a2[1] - a1[1]
  adj = math.gcd(dx, dy)
  dy //= adj
  dx //= adj
  out = set()
  startrow, start_col = a1
  r, c = startrow, start_col
  while 0 <= r < rows and 0 <= c < cols:
    out.add((r, c))
    r -= dy
    c -= dx
  r, c = startrow, start_col
  while 0 <= r < rows and 0 <= c < cols:
    out.add((r, c))
    r += dy
    c += dx
  return out

for r, line in enumerate(ant):
  for c, x in enumerate(line):
    if x == ".": continue
    antennas[x].append((r, c))

def isonmap(a):
  r, c = a
  return (0 <= r < rows) and (0 <= c < cols)

antis = set()
for ants in antennas.values():
  for a1, a2 in itertools.combinations(ants, 2):
    antis |= antinodes(a1, a2)
print(len(antis))

# 1136 too high
