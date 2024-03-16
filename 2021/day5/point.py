from dataclasses import dataclass

@dataclass
class Point:
  x: int
  y: int

  @classmethod
  def origin(cls):
    return cls(0, 0)

  @classmethod
  def parse(cls, f):
    x, y = f.split(',')
    return cls(int(x), int(y))

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return Point(self.x - other.x, self.y - other.y)

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __len__(self):
    return 1

  def __hash__(self):
    return hash((self.x, self.y))

