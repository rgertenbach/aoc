from collections import defaultdict
import itertools

with open("input.txt") as f:
  ant = f.read().strip("\n").split("\n")

rows = len(ant)
cols = len(ant[0])
antennas = defaultdict(list)

def antinodes(a1, a2):
  dx = (a2[0] - a1[0])
  dy = (a2[1] - a1[1])
  an1 = a2[0] + dx, a2[1] + dy
  an2 = a1[0] - dx, a1[1] - dy
  return an1, an2

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
    an1, an2 = antinodes(a1, a2)
    if isonmap(an1): antis.add(an1)
    if isonmap(an2): antis.add(an2)
print(len(antis))
