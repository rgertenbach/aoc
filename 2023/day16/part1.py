import sys
from enum import Enum
from typing import NamedTuple

EMPTY = '.'
R_MIRROR = '/'
L_MIRROR = '\\'
V_SPLIT = '|'
H_SPLIT = '-'

class Direction(Enum):
  UP = '^'
  DOWN = 'v'
  LEFT = '<'
  RIGHT = '>'

class Photon(NamedTuple):
  row: int
  col: int
  dir: Direction

  def move(self, dir: Direction | None = None) -> 'Photon':
    if dir is None: dir = self.dir
    if dir is Direction.UP: return Photon(self.row - 1, self.col, dir)
    if dir is Direction.DOWN: return Photon(self.row + 1, self.col, dir)
    if dir is Direction.LEFT: return Photon(self.row, self.col - 1, dir)
    return Photon(self.row, self.col + 1, dir)

  def follow(self, cave: list[str]) -> list['Photon']:
    out = []
    square = cave[self.row][self.col]
    if (
        square == EMPTY
        or (square == V_SPLIT and self.dir in {Direction.DOWN, Direction.UP})
        or (square == H_SPLIT and self.dir in {Direction.LEFT, Direction.RIGHT})):
      out.append(self.move())
    elif square == V_SPLIT:
      out.extend([self.move(Direction.UP), self.move(Direction.DOWN)])
    elif square == H_SPLIT:
      #out.extend([self.move(Direction.LEFT), self.move(Direction.RIGHT)])
      out.extend([self.move(Direction.LEFT), self.move(Direction.RIGHT)])
    elif square == R_MIRROR:
      if self.dir == Direction.UP: out.append(self.move(Direction.RIGHT))
      elif self.dir == Direction.RIGHT: out.append(self.move(Direction.UP))
      elif self.dir == Direction.DOWN: out.append(self.move(Direction.LEFT))
      elif self.dir == Direction.LEFT: out.append(self.move(Direction.DOWN))
      else: raise RuntimeError('cannot do rmirror with', self)
    elif square == L_MIRROR:
      if self.dir == Direction.UP: out.append(self.move(Direction.LEFT))
      elif self.dir == Direction.LEFT: out.append(self.move(Direction.UP))
      elif self.dir == Direction.DOWN: out.append(self.move(Direction.RIGHT))
      elif self.dir == Direction.RIGHT: out.append(self.move(Direction.DOWN))
      else: raise RuntimeError('cannot do rmirror with', self)
    else: raise RuntimeError('unsupported follow with', self)
    return [p for p in out if 0 <= p.row < len(cave) and 0 <= p.col < len(cave[0])]

def energizedf(cave: list[str], photons: set[Photon]) -> str:
  rows = []
  ps = {(p.row, p.col) for p in photons}
  for row, line in enumerate(cave):
    l = []
    for col, c in enumerate(line):
      if (row, col) in ps: l.append('#')
      else: l.append(c)
    rows.append(''.join(l))
  return '\n'.join(rows)

def energized(cave: list[str], start: Photon) -> int:
  photons = set()
  beams = [start]
  while beams:
    photon = beams.pop()
    if photon in photons: continue
    photons.add(photon)
    beams.extend(photon.follow(cave))
  return len({(p.row, p.col) for p in photons})

def part1(cave: list[str]) -> int:
  return energized(cave, Photon(0, 0, Direction.RIGHT))

def part2(cave: list[str]) -> int:
  best = 0
  for row in range(1, len(cave) - 1):
    best = max(best, energized(cave, Photon(row, 0, Direction.RIGHT)))
    best = max(best, energized(cave, Photon(row, 0, Direction.LEFT)))
    best = max(best, energized(cave, Photon(row, 0, Direction.UP)))
    best = max(best, energized(cave, Photon(row, 0, Direction.DOWN)))
    best = max(best, energized(cave, Photon(row, len(cave[0]) - 1, Direction.RIGHT)))
    best = max(best, energized(cave, Photon(row, len(cave[0]) - 1, Direction.LEFT)))
    best = max(best, energized(cave, Photon(row, len(cave[0]) - 1, Direction.UP)))
    best = max(best, energized(cave, Photon(row, len(cave[0]) - 1, Direction.DOWN)))
  for col in range(len(cave[0])):
    best = max(best, energized(cave, Photon(0, col, Direction.RIGHT)))
    best = max(best, energized(cave, Photon(0, col, Direction.LEFT)))
    best = max(best, energized(cave, Photon(0, col, Direction.UP)))
    best = max(best, energized(cave, Photon(0, col, Direction.DOWN)))
    best = max(best, energized(cave, Photon(len(cave) - 1, col, Direction.RIGHT)))
    best = max(best, energized(cave, Photon(len(cave) - 1, col, Direction.LEFT)))
    best = max(best, energized(cave, Photon(len(cave) - 1, col, Direction.UP)))
    best = max(best, energized(cave, Photon(len(cave) - 1, col, Direction.DOWN)))
  return best



def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: cave = f.read().strip().split('\n')
    print(part1(cave))
    print(part2(cave))

if __name__ == '__main__':
  main()
