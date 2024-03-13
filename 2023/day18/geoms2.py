from typing import Any, NamedTuple
from enum import Enum

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


