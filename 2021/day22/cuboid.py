import enum
import itertools
import re

from typing import Optional, List

class State(enum.Enum):
  OFF = 0
  ON = 1

  def __str__(self) -> str:
    return 'On' if self == State.ON else 'Off'


class Cuboid:
  def __init__(self, x1, x2, y1, y2, z1, z2):
    self.x1 = min(x1, x2)
    self.x2 = max(x1, x2)
    self.y1 = min(y1, y2)
    self.y2 = max(y1, y2)
    self.z1 = min(z1, z2)
    self.z2 = max(z1, z2)

  @classmethod
  def parse(cls, f) -> 'Cuboid':
    'Parses format like "x=-48..0,y=-47..2,z=-6..48"'
    x, y, z = re.findall(r'[xyz]=(-?\d+)..(-?\d+)', f)
    return cls(*(int(v) for v in itertools.chain([*x, *y, *z])))

  def __str__(self) -> str:
    return f'({self.x1}..{self.x2},{self.y1}..{self.y2},{self.z1}..{self.z2})'

  def __len__(self) -> int:
    'The number of points inside of a cuboid'
    return (
      (self.x2 - self.x1 + 1) * 
      (self.y2 - self.y1 + 1) * 
      (self.z2 - self.z1 + 1))

  def as_tuple(self):
    return (self.x1, self.x2, self.y1, self.y2, self.z1, self.z2)

  @property
  def points(self):
    for x in range(self.x1, self.x2 + 1):
      for y in range(self.y1, self.y2 + 1):
        for z in range(self.z1, self.z2 + 1):
          yield (x, y, z)


  def intersection(self, other: 'Cuboid') -> Optional['Cuboid']:
    'The cuboid of the intersection of two cuboids. None if None.'
    x1 = max(self.x1, other.x1)
    x2 = min(self.x2, other.x2)
    if x1 > x2:
      return None
    y1 = max(self.y1, other.y1)
    y2 = min(self.y2, other.y2)
    if y1 > y2:
      return None
    z1 = max(self.z1, other.z1)
    z2 = min(self.z2, other.z2)
    if z1 > z2:
      return None

    return self.__class__(x1, x2, y1, y2, z1, z2)

  def cutout(self, cut: 'Cuboid') -> List['Cuboid']:
    '''Cut a cuboid out of another one.  

    Used for OFF and turning intersections into cuboids.  
    '''
    cut = self.intersection(cut)  # We don't care about the rest.
    remaining = []
    if cut is None:
      return [self]
    # We need to check above, below, let, right front, back.
    if self.x1 < cut.x1:  # Left, up to cutout.
      remaining.append(
          self.__class__(self.x1, cut.x1 - 1, 
                         self.y1, self.y2, 
                         self.z1, self.z2))
    if self.x2 > cut.x2:  # Right, up to cutout.
      remaining.append(
          self.__class__(cut.x2 + 1, self.x2, 
                         self.y1, self.y2, 
                         self.z1, self.z2))

    x1 = max(self.x1, cut.x1)
    x2 = min(self.x2, cut.x2)

    if self.y1 < cut.y1:  # Above, down to cutouut.
      remaining.append(
        self.__class__(x1, x2, self.y1, cut.y1 - 1, self.z1, self.z2))

    if self.y2 > cut.y2:  # Below, up to cutouut.
      remaining.append(
        self.__class__(x1, x2, cut.y2 + 1, self.y2, self.z1, self.z2))

    y1 = max(self.y1, cut.y1)
    y2 = min(self.y2, cut.y2)

    if self.z1 < cut.z1:  # Behund, down to cutouut.
      remaining.append(self.__class__(x1, x2, y1, y2, self.z1, cut.z1 - 1))

    if self.z2 > cut.z2:  # In front, up to cutouut.
      remaining.append(self.__class__(x1, x2, y1, y2, cut.z2 + 1, self.z2))

    return list(remaining)

  def __add__(self, other: 'Cuboid') -> List['Cuboid']:
    'Turn cuboids on'
    others = other.cutout(self) # Remove duplicates
    return list([self]+list(others))

  
  def __sub__(self, other) -> List['Cuboid']:
    'Turn cuboids off'
    return list(self.cutout(other))


class Instruction:
  def __init__(self, cuboid, state):
    self.cuboid = cuboid
    self.state = state

  @classmethod
  def parse(cls, f):
    statef, cuboidf = f.split(' ')
    return cls(Cuboid.parse(cuboidf), State[statef.upper()])

  def __str__(self) -> str:
    return f'{str(self.state)}: {str(self.cuboid)}'
    
