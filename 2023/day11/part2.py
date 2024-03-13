from os import O_NDELAY
import sys
from typing import Iterable, NamedTuple
import itertools

SPACE = '.'
GALAXY = '#'

class Point(NamedTuple):
  row: int
  col: int

  def l1(self, other: 'Point') -> int:
    return abs(self.row - other.row) + abs(self.col - other.col)


def all_empty(xs: Iterable[str]) -> bool: return all(x == SPACE for x in xs)


def parse(universe: list[str]) -> tuple[list[Point], list[int], list[int]]:
  galaxies = []
  for row, line in enumerate(universe):
    for col, obs in enumerate(line):
      if obs == GALAXY: galaxies.append(Point(row, col))

  empty_cols = [
      row for row, line in enumerate(universe) if all_empty(line)]
  empty_rows = [
      col for col, line in enumerate(zip(*universe)) if all_empty(line)]
  return galaxies, empty_rows, empty_cols


def expand(
    galaxy: list[Point], 
    empty_rows: list[int], 
    empty_cols: list[int],
    expansion: int = 1
) -> list[Point]:
  # expand rows
  empty = 0
  new_galaxy = []
  for g in galaxy:
    while empty < len(empty_rows) and empty_rows[empty] < g.row:
      empty += 1
    new_galaxy.append(Point(g.row + empty * expansion, g.col))

  # expand columns
  galaxy = sorted(new_galaxy, key=lambda g: g.col)
  empty = 0
  new_galaxy = []
  for g in galaxy:
    while empty < len(empty_cols) and empty_cols[empty] < g.col:
      empty += 1
    new_galaxy.append(Point(g.row, g.col + empty * expansion))
  return new_galaxy


def part1(universe: list[str]) -> int:
  galaxies, empty_cols, empty_rows = parse(universe)
  galaxies = expand(galaxies, empty_rows, empty_cols)
  total = 0
  for p1, p2 in itertools.combinations(galaxies, 2):
    dist = p1.l1(p2)
    total += dist
  return total


def part2(universe: list[str]) -> int:
  galaxies, empty_cols, empty_rows = parse(universe)
  galaxies = expand(galaxies, empty_rows, empty_cols, 1_000_000 - 1)
  total = 0
  for p1, p2 in itertools.combinations(galaxies, 2):
    dist = p1.l1(p2)
    total += dist
  return total


def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f:
      universe = f.read().strip().split('\n')
    print(part1(universe))
    print(part2(universe))


if __name__ == '__main__':
  main()
