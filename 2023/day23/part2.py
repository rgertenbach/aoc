import sys
from typing import NamedTuple 
from functools import cache
sys.setrecursionlimit(10000)

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
  forks = [Point(0, 1)]
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
  forks.append(Point(trail.rows - 1, trail.cols - 2))
  return {p: i for i, p in enumerate(forks)}

def fork_is_visited(mask: int, point: Point, forks: dict[Point, int]) -> bool:
  return point in forks and bool(mask & (1 << forks[point]))

def visit_fork(mask: int, point: Point, forks: dict[Point, int]) -> int:
    return mask | (1 << forks[point])

def dists(trail: Trail, forks: dict[Point, int]) -> dict[Point, dict[Point, int]]:
  out = {}
  for src in forks:
    visited = {src}
    points = [src]
    mapping = {}
    dist = 0
    while points:
      new_points = []
      for point in points:
        if point != src and point in forks:
          mapping[point] = dist
          visited.add(point)
          continue
        visited.add(point)
        up = Point(point.row - 1, point.col)
        down = Point(point.row + 1, point.col)
        left = Point(point.row, point.col - 1)
        right = Point(point.row, point.col + 1)
        if point.row and up not in visited and trail[up] != '#': new_points.append(up)
        if point.row < trail.rows - 1 and down not in visited and trail[down] != '#': new_points.append(down)
        if point.col and left not in visited and trail[left] != '#': new_points.append(left)
        if point.col < trail.cols - 1 and right not in visited and trail[right] != '#': new_points.append(right)
      dist += 1
      points = new_points


    out[src] = mapping
  return out



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

def part2(trails: Trail) -> int:
  goal = Point(trails.rows - 1, trails.cols - 2)
  forks = find_forks(trails)
  print('  founds forks')
  distances = dists(trails, forks)
  print('  calculated dists')

  @cache
  def dfs(point: Point, distance: int, visited: int) -> int:
    if point == goal: return distance
    highest_distance = 0
    visited = visit_fork(visited, point, forks)
    for destination, additional_distance in distances[point].items():
      if fork_is_visited(visited, destination, forks): continue
      highest_distance = max(
          highest_distance,
          dfs(destination, distance + additional_distance, visited)
      )
    return highest_distance

  return dfs(Point(0, 1), 0, 1)

  
# def part2(trails: Trail) -> int:
#   goal = Point(trails.rows - 1, trails.cols - 2)
#   forks = find_forks(trails)
# 
#   # Assuming tha loops are impossible
#   @cache
#   def dfs(point: Point, last: Point, distance: int, visited: int = 0) -> int:
#     if point == goal: return distance
#     if fork_is_visited(visited, point, forks): return 0
#     if point in forks: visited = visit_fork(visited, point, forks)
#     up = Point(point.row - 1, point.col)
#     down = Point(point.row + 1, point.col)
#     left = Point(point.row, point.col - 1)
#     right = Point(point.row, point.col + 1)
#     if trails[point] == '#': return 0
#     return max(
#         0 if up == last else dfs(up, point, distance + 1, visited),
#         0 if down == last else dfs(down, point, distance + 1, visited),
#         0 if left == last else dfs(left, point, distance + 1, visited),
#         0 if right == last else dfs(right, point, distance + 1, visited))
#   
#   return dfs(Point(1, 1), Point(0, 1), 1)


def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: trails = Trail(f.read().strip().split('\n'))
    print(part1(trails))
    print(part2(trails))

if __name__ == '__main__':
  main()
