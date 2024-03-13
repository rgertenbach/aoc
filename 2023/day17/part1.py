import sys
import heapq
from typing import NamedTuple

RIGHT = '>'
LEFT = '<'
UP = '^'
DOWN = 'v'

class Path(NamedTuple):
  cost: int
  n_dir: int
  direction: str
  row: int
  col: int

  def maybe_move(
      self,
      direction: str, 
      city: list[list[int]],
      visited: set[tuple[int, int, str, int]],
      frontier: list['Path']
  ) -> None:
    if direction == RIGHT and self.direction == LEFT: return
    if direction == LEFT and self.direction == RIGHT: return
    if direction == UP and self.direction == DOWN: return
    if direction == DOWN and self.direction == UP: return
    prop_row = self.row + (1 if direction == DOWN else -1 if direction == UP else 0)
    if prop_row < 0 or prop_row >= len(city): return
    prop_col = self.col + (1 if direction == RIGHT else -1 if direction == LEFT else 0)
    if prop_col < 0 or prop_col >= len(city[0]): return
    prop_n_dir = (self.n_dir + 1) if direction == self.direction else 1 
    if prop_n_dir > 3: return
    if (prop_row, prop_col, direction, prop_n_dir) in visited: return
    prop_cost = self.cost + city[prop_row][prop_col]
    heapq.heappush(frontier, Path(prop_cost, prop_n_dir, direction, prop_row, prop_col))

def part1(city: list[list[int]]) -> int:
  rows = len(city)
  cols = len(city[0])
  visited: set[tuple[int, int, str, int]] = set()
  frontier = [Path(0, 0, RIGHT, 0, 0)]
  heapq.heapify(frontier)
  while frontier:
    path = heapq.heappop(frontier)
    cost, n_dir, direction, row, col = path
    if (row == rows - 1 and col == cols - 1): return cost
    if (row, col, direction, n_dir) in visited: continue
    visited.add((row, col, direction, n_dir))
    path.maybe_move(LEFT, city, visited, frontier)
    path.maybe_move(RIGHT, city, visited, frontier)
    path.maybe_move(UP, city, visited, frontier)
    path.maybe_move(DOWN, city, visited, frontier)
  return -1

def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: city_raw = f.read().strip().split('\n')
    city = [list(map(int, line)) for line in city_raw]
    print(part1(city))

if __name__ == '__main__':
  main()
