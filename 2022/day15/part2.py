from typing import Optional
from collections import namedtuple
import re

Point = namedtuple('Point', ['x', 'y'])
Orth = namedtuple('Orth', ['x', 'off'])
Cover = namedtuple('Cover', ['left', 'right'])


def load(filename: str):
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


def tuning_freq(beacon: Point) -> int:
  return 4_000_000 * beacon.x + beacon.y


def gaps(coverages, min_x: int, max_x: int) -> list[int]:
  out = []
  if coverages[0].left > min_x:
    print('adding to the left')
    out.extend(list(range(min_x, coverages[0].x)))
  if coverages[-1].right < max_x:
    print('adding to the right')
    out.extend(list(range(coverages[-1].x + 1, max_x + 1)))
  if len(coverages) > 1:
    print('adding gaps')
    for left, right in zip(coverages[:-1], coverages[1:]):
      out.extend(list(range(left.right + 1, right.left, 1)))
  return sorted(out)



def uncovered(reads, row: int, max_coord: int) -> Optional[int]:
  """# of impossible points on row IF IT FUCKING WORKED!!!!"""
  orths = [make_orth(sensor, beacon, row) for sensor, beacon in reads]
  orth_on_row = [o for o in orths if o.off >= 0]
  covered = [cover_from_orth(orth) for orth in orth_on_row]
  reduced = merge_covers(covered)
  g = gaps(reduced, 0, max_coord)
  if g:
    if len(g) > 1:
      raise ValueError(f'Too many gaps: {g}')
    return g[0]

  return None


def find_tuning_freq(filename: str, max_coord: int) -> int:
  reads = load(filename)
  for row in range(max_coord + 1):
    if row % 10_000 == 0:
      print(f'{row} / {max_coord}')
    gap = uncovered(reads, row, max_coord)
    if gap is not None:
      print(gap)
      return tuning_freq(Point(gap, row))
  raise RuntimeError('No gaps found')



if __name__ == '__main__':
  print('Test')
  print(find_tuning_freq('test_input.txt', 20))

  print('\nActual')
  print(find_tuning_freq('input.txt', 4_000_000))
