from enum import Enum
from dataclasses import dataclass
from typing import Iterable, List

class Axis(Enum):
  X = 1
  Y = 2
  Z = 3

@dataclass
class Point:
  x: int
  y: int
  z: int

  @classmethod
  def from_tuple(cls, t):
    return cls(t[0], t[1], t[2])

  def as_tuple(self):
    return self.x, self.y, self.z

  def __hash__(self):
    return hash(self.as_tuple())

  def copy(self) -> 'Point':
    return self.__class__(self.x, self.y, self.z)

  def __neg__(self) -> 'Point':
    return self.__class__(-self.x, -self.y, -self.z)

  def __add__(self, other) -> 'Point':
    return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

  def __sub__(self, other) -> 'Point':
    return self + -other

  def __str__(self) -> str:
    return f'({self.x},{self.y},{self.z})'

  def __eq__(self, other) -> bool:
    return self.x == other.x and self.y == other.y and self.z == other.z
  
class Beacon(Point):

  def rotate(self, axis):
    if axis == Axis.Y:
      return self.__class__(self.z, self.y, -self.x)
    if axis == Axis.X:
      return self.__class__(self.x, -self.z, self.y)
    if axis == Axis.Z:
      return self.__class__(-self.y, self.x, self.z)

  def rotations(self, axis):
    return [
      self.copy(), 
      self.rotate(axis), 
      self.rotate(axis).rotate(axis), 
      self.rotate(axis).rotate(axis).rotate(axis)
    ]


  def permutations(self) -> List['Beacon']:
    'List of all possibel permutations.'
    faces = [
        self.__class__(self.x, self.y, self.z),
        self.__class__(self.z, self.y, -self.x),
        self.__class__(-self.x, self.y, -self.z),
        self.__class__(-self.z, self.y, self.x),
        self.__class__(self.x, self.z, -self.y),
        self.__class__(self.z, -self.z, self.y),
    ]
    return [
      rot
      for face in faces
      for rot in face.rotations(Axis.Z)
    ]


def point_matches(ps1: Iterable[Point], ps2: Iterable[Point]) -> List[Point]:
  matches = []
  for p1 in ps1:
    for p2 in ps2:
      if p1 == p2:
        matches.append(p1)
        break
  return matches
