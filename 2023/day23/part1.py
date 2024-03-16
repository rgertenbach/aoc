import sys
from typing import NamedTuple 
from functools import cache
sys.setrecursionlimit(40000)

class Point(NamedTuple):
  row: int
  col: int

class Trail:
  def __init__(self, trails: list[str]): self.trails = trails
  def __getitem__(self, idx: tuple[int, int]) -> str: 
    return self.trails[idx[0]][idx[1]]
  @property
  def rows(self) -> int: return len(self.trails)
  @property
  def cols(self) -> int: return len(self.trails[0])

def find_forks(trail: Trail) -> dict[Point, int]:
  forks = []
  for row, line in enumerate(trail.trails):
    for col, c in enumerate(line):
      if c == '#': continue
      if col == 0 or col >= trail.cols - 1: continue
      if row == 0 or row >= trail.rows - 1: continue
      total = 0
      if trail[Point(row-1, col)] != '#': total += 1
      if trail[Point(row+1, col)] != '#': total += 1
      if trail[Point(row, col-1)] != '#': total += 1
      if trail[Point(row, col+1)] != '#': total += 1
      if total >= 3: forks.append(Point(row, col))
  return {p: i for i, p in enumerate(forks)}

def fork_is_visited(mask: int, point: Point, forks: dict[Point, int]) -> bool:
  return point in forks and bool(mask & (1 << forks[point]))

def visit_fork(mask: int, point: Point, forks: dict[Point, int]) -> int:
    return mask | (1 << forks[point])


def part1(trails: Trail) -> int:
  goal = Point(trails.rows - 1, trails.cols - 2)
  forks = find_forks(trails)

  # Assuming tha loops are impossible
  @cache
  def dfs(point: Point, last: Point, distance: int, visited: int = 0) -> int:
    if point == goal: return distance
    if fork_is_visited(visited, point, forks): return 0
    if point in forks: visited = visit_fork(visited, point, forks)
    up = Point(point.row - 1, point.col)
    down = Point(point.row + 1, point.col)
    left = Point(point.row, point.col - 1)
    right = Point(point.row, point.col + 1)
    match trails[point]:
      case '^': return dfs(up, point, distance + 1, visited)
      case 'v': return dfs(down, point, distance + 1, visited)
      case '<': return dfs(left, point, distance + 1, visited)
      case '>': return dfs(right, point, distance + 1, visited)
      case '#': return 0
      case _: return max(
          0 if up == last or trails[up] == 'v' else dfs(up, point, distance + 1, visited),
          0 if down == last or trails[down] == '^' else dfs(down, point, distance + 1, visited),
          0 if left == last or trails[left] == '>' else dfs(left, point, distance + 1, visited),
          0 if right == last or trails[right] == '<' else dfs(right, point, distance + 1, visited))
  
  return dfs(Point(1, 1), Point(0, 1), 1)

  


def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: trails = Trail(f.read().strip().split('\n'))
    print(part1(trails))

if __name__ == '__main__':
  main()
