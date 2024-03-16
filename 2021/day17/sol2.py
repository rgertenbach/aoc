#!/usr/bin/python3

import sys
import re
from dataclasses import dataclass

def sign(x):
  if x > 0:
    return 1
  if x < 0:
    return -1
  if x == 0:
    return 0
  raise ValueError('Not a valid input')

def sumtox(x):
  return x * (x + 1) // 2

def x_for_sumto(n):
  y = n * 2
  return int(y**(1/2))


@dataclass
class Point:
  x: int
  y: int

@dataclass
class Probe:
  pos: Point = None
  dx: int = 0
  dy: int = 0

  def shoot(self, vel):
    self.pos = Point(0,0)  
    dx, dy = vel
    self.dx = dx
    self.dy = dy
    yield self.pos
    while True:
      self.pos.x += self.dx
      self.pos.y += self.dy
      yield self.pos
      self.dx = sign(self.dx) * (abs(self.dx) - 1)
      self.dy -= 1

  def check_hit(self, vel, target) -> bool:
    arc = self.shoot(vel)
    while True:
      pos = next(arc)
      if target.contains(pos):
        return True
      if pos.x > target.bottom_right.x or (pos.y < target.bottom_right.y and self.dy <= 0):
        return False


def y_after_steps(dy, nsteps):
  # y = dy * n - (n * (n - 1) // 2)  
  return dy * nsteps - sumtox(nsteps - 1)


@dataclass
class Rect:
  top_left: Point
  bottom_right: Point

  @classmethod
  def parse(cls, f):
    coords = re.findall(r'.*x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', f)[0]
    x1, x2, y1, y2 = [int(coord) for coord in coords]
    top_left = Point(min(x1, x2), max(y1, y2))
    bottom_right = Point(max(x1, x2), min(y1, y2))
    return cls(top_left, bottom_right)

  def contains(self, point: Point) -> bool:
    return (point.x >= self.top_left.x and point.x <= self.bottom_right.x
            and point.y <= self.top_left.y and point.y >= self.bottom_right.y)

def find_max(rect):
  max_dx = rect.bottom_right.x
  min_dx = x_for_sumto(rect.top_left.x)
  probe = Probe()
  print(min_dx, max_dx)
  for dx in range(min_dx, max_dx + 1):
    min_n_steps = dx  # !
    for dy in range(1000, -1000, -1):
      if probe.check_hit((dx, dy), rect):
        yield (dx, dy)


def read_file(filename):
  with open(filename) as f:
    line = f.readline()
  return Rect.parse(line)

target = read_file(sys.argv[1])


maxvel = list(find_max(target))
print(len(maxvel))
  

