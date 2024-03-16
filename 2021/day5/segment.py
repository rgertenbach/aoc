from dataclasses import dataclass
from enum import Enum
from point import Point
from typing import Tuple

def _between(x, x1, x2):
  return x >= min(x1, x2) and x <= max(x1, x2)

def sign(x):
  if x > 0:
    return 1
  if x < 0:
    return -1
  return 0

class Direction:
  HORIZONTAL = 1
  VERTICAL = 2
  DIAGONAL = 3


class Segment:
  def __init__(self, p1, p2):
    if p2.x < p1.x:
      p1, p2 = p2, p1
    elif p2.y < p1.y:
      p1, p2 = p2, p1
    self.p1 = p1
    self.p2 = p2

  @classmethod
  def parse(cls, s):
    s1, s2 = s.strip().split(' -> ')
    p1 = Point.parse(s1)
    p2 = Point.parse(s2)
    return cls(p1, p2)

  def offset(self, offset: Point):
    p1 = self.p1 - offset
    p2 = self.p2 - offset
    return self.__class__(p1, p2)

  @property
  def direction(self):
    c, off = self.center()
    if c.p2.x and c.p2.y:
      return Direction.DIAGONAL
    if c.p2.x:
      return Direction.HORIZONTAL
    return Direction.VERTICAL

  def center(self) -> Tuple["Segment", Point]:
    offset = self.p1
    out = self.__class__(Point.origin(), self.p2 - offset)
    return out, offset

  def points(self):
    c, off = self.center()
    if c.p2.x == 0:
      return [Point(0, y) + off for y in range(c.p2.y + 1)]
    if c.p2.y == 0:
      return [Point(x, 0) + off for x in range(c.p2.x + 1)]
        

  def overlaps(self, other):  # None, [Point]
    c, off = self.center()
    o = other.offset(off)
    overlaps = []
    
    if o.p2.x < c.p1.x or o.p1.x > c.p2.x:  # All left
      return overlaps
    if o.p2.y < c.p1.y or o.p1.y > c.p2.y: 
      return overlaps

    for cp in c.points():
      for op in o.points():
        if cp == op:
          overlaps.append(cp)
    return [overlap + off for overlap in overlaps]
