#!/usr/bin/python3
# Should give 5 / 5092
# We only care about straights and diagonals!

from dataclasses import dataclass
from typing import Tuple
import enum
import sys


@dataclass
class Point:
  x: int
  y: int

  @classmethod 
  def origin(cls):
    return cls(0, 0)

  @classmethod
  def from_segment(cls, segment):
    x, y = segment.split(',')
    return cls(int(x), int(y))

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return Point(self.x - other.x, self.y - other.y)

  def __len__(self):
    return 1


class Direction(enum.Enum):
  HORIZONTAL = 1
  VERTICAL = 2
  DIAGONAL = 3

  
@dataclass
class Line:
  p1: Point
  p2: Point

  def intersection(self, other):
    offset = self.p1
    n1 = Line(Point.origin(), self.p2 - p1)
    n2 = Line(other.p1 - p1, other.p2 - p1)
    pass

  @classmethod
  def parse(cls, s):
    s1, s2 = s.strip().split(' -> ')
    p1 = Point.from_segment(s1)
    p2 = Point.from_segment(s2)
    return cls(p1, p2)

  def offset(self, offset: Point):
    p1 = self.p1 - offset
    p2 = self.p2 - offset
    return self.__cls__(p1, p2)

  def center(self) -> Tuple["Line", Point]:
    offset = self.p1
    output = self.__cls__(Point.origin(), self.p2 - offset)
    return output, offset

  @property
  def is_straight(self):
    return self.p1.x == self.p2.x or self.p1.y == self.p2.y

  @property
  def direction(self) -> Direction:
    l, _ = self.center()
    v = l.p2
    if v.x and v.y:
      return Direction.DIAGONAL
    elif v.x:
      return Direction.HORIZONTAL
    else:
      return Direction.VERTICAL


  def overlap(self, other):
    centered, offset = self.centered
    other = other.offset(offset)
    if centered.direction == other.direction:
      if (centered.direction == Direction.HORIZONTAL):
      else return 0

    else:
      # check for intersection
      pass

  def __len__(self):
    centered, offset = self.centered
    return max(centered.p2.x, centered.p2.y)







def load_data(filename):
  vents = []
  with open(filename) as f:
    for line in f:
      vents.append(Line.parse(line))
  return vents


if __name__ == '__main__':
  vents = load_data(sys.argv[1])
  straight_vents = [vent for vent in vents if vent.is_straight]
  print(straight_vents[0])
  



