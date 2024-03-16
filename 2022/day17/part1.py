from typing import Iterator, Iterable, Callable
from collections import namedtuple


Point = namedtuple('Point', ['x', 'y'])
XL = 2
WIDTH = 7


def movegen(filepath: str):
  with open(filepath) as f:
    moves = f.read().strip()

  while True:
    yield from moves


def highest(pile: set) -> int:
  return max(pile, key=lambda p: p.y).y + 1 if pile else 0


class Shape:
  def __init__(self, points: Iterable[Point]):
    self.points = tuple(points)

  def move(self, direction: str, pile: set) -> 'Shape':
    if direction == '>':
      if max(self.points, key=lambda p: p.x).x == WIDTH - 1:
        return self
      dest = Shape(Point(p.x  + 1, p.y) for p in self.points)
      if any(p in pile for p in dest.points):
        return self
      return dest

    if direction == '<':
      if min(self.points, key=lambda p: p.x).x == 0:
        return self
      dest = Shape(Point(p.x  - 1, p.y) for p in self.points)
      if any(p in pile for p in dest.points):
        return self
      return dest

    dest = Shape(Point(p.x, p.y - 1) for p in self.points)
    if any(p in pile for p in dest.points) or min(self.points, key=lambda p: p.y).y == 0:
      return self
    return dest


  @classmethod
  def make_minus(cls, pile) -> 'Shape':
    y = highest(pile) + 3
    return cls([Point(XL, y), Point(XL + 1, y), Point(XL + 2, y), Point(XL + 3, y)])

  @classmethod
  def make_plus(cls, pile) -> 'Shape':
    y = highest(pile) + 3
    return cls([Point(XL + 1, y), Point(XL, y + 1), Point(XL + 1, y + 1), Point(XL + 2, y + 1), Point(XL + 1, y + 2)])


  @classmethod
  def make_l(cls, pile) -> 'Shape':
    y = highest(pile) + 3
    return cls([Point(XL, y), Point(XL + 1, y), Point(XL + 2, y), Point(XL + 2, y + 1), Point(XL + 2, y + 2)])

  @classmethod
  def make_bar(cls, pile) -> 'Shape':
    y = highest(pile) + 3
    return cls([Point(XL, y), Point(XL, y + 1), Point(XL, y + 2), Point(XL, y + 3)])

  @classmethod
  def make_square(cls, pile) -> 'Shape':
    y = highest(pile) + 3
    return cls([Point(XL, y), Point(XL + 1, y), Point(XL, y + 1), Point(XL + 1, y + 1)])


def piecegen() -> Iterator[Callable[[set], Shape]]:
  shapes = [Shape.make_minus, Shape.make_plus, Shape.make_l, Shape.make_bar, Shape.make_square]
  while True:
    for shape in shapes:
      yield lambda pile: shape(pile)



def plot(piece, pile):
  maxy = max(piece.points, key=lambda p: p.y).y
  lines = []
  for i in range(maxy + 1):
    line = []
    for c in range(WIDTH):
      if Point(c, i) in piece.points:
        line.append('@')
      elif Point(c, i) in pile:
        line.append('#')
      else:
        line.append('.')
    lines.append('|' + ''.join(line) + '|')
  print('\n'.join(lines[::-1]) + '\n+' + '-' * WIDTH + '+\n')

def main():
  moves = movegen('input.txt')
  pieces = piecegen()
  pile = set()
  n_generated = 0
  steps = 0

  while True:
    piece = next(pieces)(pile)
    n_generated += 1
    if n_generated == 2023:
      break
    while True:
      steps = steps + 1
      piece = piece.move(next(moves), pile)
      dest = piece.move('down', pile)
      if dest == piece:
        break
      piece = dest
    for point in piece.points:
      pile.add(point)
      


  print(highest(pile))
  

if __name__ == '__main__':
  main()


