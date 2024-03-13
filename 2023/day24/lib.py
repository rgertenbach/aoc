from typing import NamedTuple

class Vector(NamedTuple):
  x: int | float
  y: int | float
  z: int | float | None = None

  @classmethod
  def parse(cls, s: str) -> 'Vector':
    x, y, z = s.split(', ')
    return cls(int(x), int(y), int(z))

  @property
  def is_2d(self) -> bool: return self.z is None

  def __str__(self) -> str:
    if self.is_2d: return f'{self.x}, {self.y}'
    return f'{self.x}, {self.y}, {self.z}'
  
  def slope(self, other: 'Vector') -> 'Vector':
    dx = other.x - self.x
    dy = other.y - self.y
    if self.z is None != other.z is None:
      raise ValueError(f'Incompatible {self} and {other}')
    if self.z is None or other.z is None: return Vector(1, dy / dx)
    dz = other.z - self.z
    return Vector(1, dy / dx, dz / dx)

  def normalize(self) -> 'Vector':
    dz = None if self.z is None else self.z / self.x
    return Vector(self.x, self.y / self.x, dz)

  def __round__(self, digits: int) -> 'Vector':
    z = None if self.is_2d is None else round(self.z, digits)
    return Vector(round(self.x, digits), round(self.y, digits), z)
  
  def __add__(self, other: 'Vector') -> 'Vector':
    if self.is_2d != other.is_2d: raise RuntimeError(f'Incompatible vectors {self} and {other}')
    z = None if self.z is None else self.z + other.z
    return self.__class__(self.x + other.x, self.y + other.y, z)

  def __sub__(self, other: 'Vector') -> 'Vector':
    if self.is_2d != other.is_2d: raise RuntimeError(f'Incompatible vectors {self} and {other}')
    z = None if self.z is None else self.z - other.z
    return self.__class__(self.x - other.x, self.y - other.y, z)

  def __neg__(self) -> 'Vector':
    z = None if self.z is None else -self.z
    return self.__class__(-self.x, -self.y, z)


class Stone(NamedTuple):
  pos: Vector
  speed: Vector

  def __str__(self) -> str: return f'{self.pos} @ {self.speed}'

  @classmethod
  def parse(cls, s: str) -> 'Stone':
    pos, spd = s.split(' @ ')
    return cls(Vector.parse(pos), Vector.parse(spd))

  @property
  def intercept_slope_xy(self) -> tuple[float, float]:
    # y intercept and slope per x change
    slope = self.speed.y / self.speed.x
    intercept = self.pos.y - slope * self.pos.x
    return intercept, slope

  def position_at(self, time: int) -> Vector:
    x = self.pos.x + time * self.speed.x
    y = self.pos.y + time * self.speed.y
    if self.pos.z is None or self.speed.z is None: return Vector(x, y)
    return Vector(x, y, self.pos.z + time * self.speed.z)

  def intersects_xy(self, other) -> Vector | None:
    i1, s1 = self.intercept_slope_xy
    i2, s2 = other.intercept_slope_xy
    if s1 == s2: return None
    intersect_x = (i1 - i2) / (s2 - s1)
    if intersect_x < self.pos.x and self.speed.x >= 0: return None
    if intersect_x < other.pos.x and other.speed.x >= 0: return None
    if intersect_x > self.pos.x and self.speed.x <= 0: return None
    if intersect_x > other.pos.x and other.speed.x <= 0: return None
    # in the past?
    x_change = intersect_x - self.pos.x
    intersect_y = self.pos.y + x_change * s1
    return Vector(intersect_x, intersect_y)
