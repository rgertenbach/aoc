import sys
from typing import NamedTuple
from enum import Enum
from collections import Counter

class Turn(Enum):
  LEFT = 1
  RIGHT = 2
  U = 3
  STRAIGHT = 4

class Direction(Enum):
  DOWN = 'D'
  UP = 'U'
  LEFT = 'L'
  RIGHT = 'R'

  @property
  def opposite(self) -> 'Direction':
    if self is Direction.DOWN: return Direction.UP
    if self is Direction.UP: return Direction.DOWN
    if self is Direction.LEFT: return Direction.RIGHT
    if self is Direction.RIGHT: return Direction.LEFT
    raise RuntimeError('Incompatible:', self)

  def turns(self, other: 'Direction') -> Turn:
    if self is other: return Turn.STRAIGHT
    if self is other.opposite: return Turn.U
    if (self, other) in {
        (Direction.LEFT, Direction.UP),
        (Direction.UP, Direction.RIGHT),
        (Direction.RIGHT, Direction.DOWN), 
        (Direction.DOWN, Direction.LEFT)
    }: return Turn.RIGHT
    return Turn.LEFT


class Dig(NamedTuple):
  dir: Direction
  amt: int
  col: str

  @classmethod
  def parse(cls, s: str) -> 'Dig':
    d, a, c = s.split(' ')
    return cls(Direction(d), int(a), c.strip('()'))

class Point(NamedTuple):
  row: int
  col: int

  def up(self) -> 'Point': return Point(self.row - 1, self.col)
  def down(self) -> 'Point': return Point(self.row + 1, self.col)
  def left(self) -> 'Point': return Point(self.row, self.col - 1)
  def right(self) -> 'Point': return Point(self.row, self.col + 1)
  def move(self, direction: Direction) -> 'Point':
    if direction is Direction.UP: return self.up()
    if direction is Direction.DOWN: return self.down()
    if direction is Direction.LEFT: return self.left()
    if direction is Direction.RIGHT: return self.right()

  def to_the(self, direction: Direction, side: Turn) -> 'Point':
    if direction is Direction.UP: return self.left() if side is Turn.LEFT else self.right()
    if direction is Direction.DOWN: return self.right() if side is Turn.LEFT else self.left()
    if direction is Direction.RIGHT: return self.up() if side is Turn.LEFT else self.down()
    if direction is Direction.LEFT: return self.down() if side is Turn.LEFT else self.up()



def flood_fill(lagoon: set[Point], start: Point) -> None:
  stack = [start]
  while stack:
    p = stack.pop()
    if p in lagoon: continue
    lagoon.add(p)
    if p.up() not in lagoon: stack.append(p.up())
    if p.down() not in lagoon: stack.append(p.down())
    if p.left() not in lagoon: stack.append(p.left())
    if p.right() not in lagoon: stack.append(p.right())


def part1(dig_plan: list[Dig]) -> int:
  point = Point(0, 0)
  path = {point}
  last = Direction.RIGHT
  turns = Counter()

  for dig in dig_plan:
    turns[last.turns(dig.dir)] += 1
    last = dig.dir
    for _ in range(dig.amt):
      point = point.move(dig.dir)
      path.add(point)

  direction = Turn.LEFT if turns[Turn.LEFT] > turns[Turn.RIGHT] else Turn.RIGHT
  lagoon = {p for p in path}
  point = Point(0, 0)
  for dig in dig_plan:
    for _ in range(dig.amt):
      flood_fill(lagoon, point.to_the(dig.dir, direction))
      point = point.move(dig.dir)

  return len(lagoon)

def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: data = f.read().strip().split('\n')
    dig_plan = [Dig.parse(dig) for dig in data]
    print(part1(dig_plan))


if __name__ == '__main__':
  main()
