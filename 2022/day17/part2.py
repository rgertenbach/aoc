from typing import Iterator, Iterable, Callable
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt


Point = namedtuple('Point', ['x', 'y'])
XL = 2
WIDTH = 7
N_SHAPES = 5


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


def find_min_seq(s):
  slen = len(s)
  for offset in range(slen - 2):
    if offset % 10 == 0:
      print(f'Trying {offset=}')
    ss = s[offset:]
    sslen = len(ss)

    for l in range(1, sslen // 2):
      # if l % 100 == 0:
      #   print(f'Trying length {l}')
      seq = ss[:l]
      newseq = np.tile(seq, sslen // l)
      rem = seq[:sslen % l]
      test_seq = np.concatenate([newseq, rem])
      if np.all(test_seq == ss):
        return seq, offset
  return None, None


def max_height(filename: str, training_shapes: int = 5000) -> int:
  next_move = movegen(filename)
  pieces = piecegen()
  pile = set()
  n_generated = 0
  steps = 0
  heights = []

  max_steps = 1_000_000_000_000
  while True:
    piece = next(pieces)(pile)
    n_generated += 1
    if n_generated == 5000:
      break
    while True:
      steps = steps + 1
      piece = piece.move(next(next_move), pile)
      dest = piece.move('down', pile)
      if dest == piece:
        break
      piece = dest
    for point in piece.points:
      pile.add(point)
    if n_generated % 1000 == 0:
      print(f'{n_generated=}')


    heights.append(highest(pile))
      
  print('finished sims')
  heights = np.array(heights)
  diffs = heights[1:] - heights[:-1]
  print('finding shortest repeating sequence')
  seq, off = find_min_seq(np.array(diffs))
  print(seq, off)
  if seq is None:
    print('fuu')
  inc_per_seq = np.sum(seq)
  full_seqs = (max_steps - off) // len(seq)
  reml = max_steps - off - full_seqs * len(seq)
  remainder = seq[:reml]
  return np.sum(diffs[:off]) + full_seqs * inc_per_seq + np.sum(remainder)



def main():
  print('Test')
  test = max_height('test_input.txt') 
  if test == 1514285714288:
    print('Test Passed!')
  else:
    print('Test FAILED!')

  print('\nProd')
  answer = max_height('input.txt')
  print(answer)
  if answer < 1500874634865:
    print('too low')
  if answer == 1500874634865:
    print('old')


if __name__ == '__main__':
  main()


