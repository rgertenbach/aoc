from typing import Any, NamedTuple
from enum import Enum

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

  def proper(self) -> 'Dig':
    d = {'0': Direction.RIGHT, '1': Direction.DOWN, '2': Direction.LEFT, '3': Direction.UP}[self.col[-1]]
    a = int(self.col[1:-1], 16)
    return Dig(d, a, '')


class Point(NamedTuple):
  row: int
  col: int

  def __str__(self) -> str:
    return f'({self.row},{self.col})'

  def __repr__(self) -> str:
    return str(self)

  def up(self, amt: int = 1) -> 'Point': return Point(self.row - amt, self.col)
  def down(self, amt: int = 1) -> 'Point': return Point(self.row + amt, self.col)
  def left(self, amt: int = 1) -> 'Point': return Point(self.row, self.col - amt)
  def right(self, amt: int = 1) -> 'Point': return Point(self.row, self.col + amt)
  def move(self, direction: Direction, amt: int = 1) -> 'Point':
    if direction is Direction.UP: return self.up(amt)
    if direction is Direction.DOWN: return self.down(amt)
    if direction is Direction.LEFT: return self.left(amt)
    if direction is Direction.RIGHT: return self.right(amt)

  def to_the(self, direction: Direction, side: Turn) -> 'Point':
    if direction is Direction.UP: return self.left() if side is Turn.LEFT else self.right()
    if direction is Direction.DOWN: return self.right() if side is Turn.LEFT else self.left()
    if direction is Direction.RIGHT: return self.up() if side is Turn.LEFT else self.down()
    if direction is Direction.LEFT: return self.down() if side is Turn.LEFT else self.up()


class Line(NamedTuple):
  p1: Point
  p2: Point

  @property
  def direction(self) -> Direction:
    if self.p2.row < self.p1.row: return Direction.UP
    if self.p2.row > self.p1.row: return Direction.DOWN
    if self.p2.col < self.p1.col: return Direction.LEFT
    return Direction.RIGHT

  def __len__(self) -> int:
    return abs(self.p1.row - self.p2.row) + abs(self.p1.col - self.p2.col) + 1

class Rectangle(NamedTuple):
  p1: Point
  p2: Point

  @property
  def area(self) -> int:
    return (abs(self.p1.row - self.p2.row) + 1) * (abs(self.p1.col - self.p2.col) + 1)

