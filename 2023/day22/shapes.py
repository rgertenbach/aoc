from typing import NamedTuple
from dataclasses import dataclass

class Point(NamedTuple):
  x: int
  y: int
  z: int  # vertical

  @classmethod
  def parse(cls, s: str) -> 'Point':
    return cls(*(int(x) for x in s.split(',')))

  def drop(self, n: int = 1) -> 'Point':
    return self.__class__(self.x, self.y, self.z - n)

  def __str__(self) -> str:
    return f'({self.x},{self.y},{self.z})'

@dataclass
class Brick:
  p1: Point
  p2: Point

  @classmethod
  def parse(cls, s: str) -> 'Brick':
    return cls(*(Point.parse(x) for x in s.split('~')))

  @property
  def lowest_point(self) -> int: return min(self.p1.z, self.p2.z)
  @property
  def highest_point(self) -> int: return max(self.p1.z, self.p2.z)

  def __repr__(self) -> str:
    return f'[{self.p1}~{self.p2}]'

  def drop(self, n: int = 1) -> None:
    self.p1 = self.p1.drop(n)
    self.p2 = self.p2.drop(n)

  def is_above(self, other: 'Brick') -> bool:
    # Points in bricks or top-left first.
    if self.p1.x > other.p2.x or other.p1.x > self.p2.x: return False
    if self.p1.y > other.p2.y or other.p1.y > self.p2.y: return False
    return True

