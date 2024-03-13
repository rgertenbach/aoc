import sys
from functools import cache

START = 'S'
PLOT = '.'
ROCK = '#'

Point = tuple[int, int]

class Garden:
  def __init__(self, garden: list[list[str]]) -> None:
    self.garden = garden
    self.rows = len(garden)
    self.cols = len(garden[0])
    self.start = find_start(garden)

  def __getitem__(self, rc: Point) -> str:
    row = rc[0] % self.rows
    col = rc[1] % self.rows
    return self.garden[row][col]

  @cache
  def visitable(self, rc: Point) -> set[Point]:
    row, col = rc
    out = set()
    if self[row-1, col] != ROCK: out.add((row - 1, col))
    if self[row+1, col] != ROCK: out.add((row + 1, col))
    if self[row, col-1] != ROCK: out.add((row, col - 1))
    if self[row, col+1] != ROCK: out.add((row, col + 1))
    return out

def visitable_spaces(garden: Garden, steps: int) -> list[int]:
  out = [1]
  spaces: set[Point] = {garden.start}
  for i in range(steps):
    print(f'\r{i}', end='')
    new_spaces = set()
    for start in spaces: new_spaces.update(garden.visitable(start))
    spaces = new_spaces
    out.append(len(spaces))
  print()
  return out


def find_start(garden: list[list[str]]) -> Point:
  start_row = -1
  start_col = -1
  for row, line in enumerate(garden):
    for col, c in enumerate(line):
      if c == START:
        start_row = row
        start_col = col
        break;
  if start_row + start_col < 0: raise RuntimeError()
  return start_row, start_col


def part1(garden: list[list[str]]) -> int:
  pos = [find_start(garden)]
  for _ in range(64):
    new_pos = set()
    for row, col in pos:
      if row and garden[row - 1][col] != ROCK: new_pos.add((row - 1, col))
      if row < len(garden) - 1 and garden[row + 1][col] != ROCK: new_pos.add((row + 1, col))
      if col and garden[row][col - 1] != ROCK: new_pos.add((row, col - 1))
      if col < len(garden[0]) - 1 and garden[row][col + 1] != ROCK: new_pos.add((row, col + 1))
    pos = list(new_pos)
  return len(pos)


def part2(garden: Garden) -> int:
  #visitable = visitable_spaces(garden, 1200)
  visitable = visitable_spaces(garden, 30)
  print(visitable)
  return 0


def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: data = f.read().strip()
    garden = Garden([list(row) for row in data.split('\n')])
    #print(part1(garden.garden))
    print(part2(garden))


if __name__ == '__main__':
  main()

