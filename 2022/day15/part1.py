from typing import Optional
from collections import namedtuple
import re

Point = namedtuple('Point', ['x', 'y'])
Orth = namedtuple('Orth', ['x', 'off'])
Cover = namedtuple('Cover', ['left', 'right'])


def load(filename: str) -> list[tuple[Point, Point]]:
  """Load file into a list of tuples of Sensor and beacon points."""
  with open(filename) as f:
    reads = f.readlines()
  reads = [re.findall(r'-?\d+', read) for read in reads]
  return [
      (Point(int(sx), int(sy)), Point(int(bx), int(by))) 
      for sx, sy, bx, by in reads]


def l1(p1: Point, p2: Point) -> int:
  """Manhattan Distance between two points"""
  x = abs(max(p1.x, p2.x) - min(p1.x, p2.x))
  y = abs(max(p1.y, p2.y) - min(p1.y, p2.y))
  return x + y


def make_orth(sensor: Point, beacon: Point, row: int) -> Orth:
  """X position of the sensor and amount the range spans on the row"""
  dist_to_beacon = l1(sensor, beacon)
  dist_to_row = l1(sensor, Point(sensor.x, row))
  off = dist_to_beacon - dist_to_row
  return Orth(sensor.x, off)


def cover_from_orth(orth: Orth) -> Cover:
  """Left and right most x-coordinates of an Orthogonal"""
  return Cover(orth.x - orth.off, orth.x + orth.off)


def merge_coverage(left: Cover, right: Cover) -> tuple[Cover, Optional[Cover]]:
  """Merges two covers if the left one overlaps the right start"""
  if left.right < right.left - 1:
    return left, right
  return Cover(left.left, max(left.right, right.right)), None


def width(cover: Cover) -> int:
  """Amount of space covered"""
  return cover.right - cover.left + 1


def merge_covers(covered: list[Cover]) -> list[Cover]:
  """Merges all covers into the smallest possible list of covers"""
  covered = sorted(covered)
  reduced = []
  left = covered[0]
  for right in covered[1:]:
    left, right = merge_coverage(left, right)
    if right is not None:
      reduced.append(left)
      left = right
  reduced.append(left)
  return reduced


def n_impossible(filename: str, row: int) -> int:
  """# of impossible points on row IF IT FUCKING WORKED!!!!"""
  reads = load(filename)
  x_on_row = set(beacon.x for _, beacon in reads if beacon.y == row)
  orths = [make_orth(sensor, beacon, row) for sensor, beacon in reads]
  # for x in orths:
  #   print(x)
  orth_on_row = [o for o in orths if o.off >= 0]
  covered = [cover_from_orth(orth) for orth in orth_on_row]
  reduced = merge_covers(covered)
  print(reduced)
  return sum(width(cover) for cover in reduced) - len(x_on_row)


if __name__ == '__main__':
  print('Test')
  print(n_impossible('test_input.txt', 10))

  print('\nActual')
  print(n_impossible('input.txt', 2_000_000))
  # 4704090 is not the answer...
  # want 4886370
