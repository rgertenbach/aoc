import sys
Point = tuple[int, int]

NORTH_SOUTH = '|'
EAST_WEST = '-'
NORTH_EAST = 'L'
NORTH_WEST = 'J'
SOUTH_WEST = '7'
SOUTH_EAST = 'F'
START = 'S'
GROUND = '.'


def find_start(pipes: list[str]) -> Point:
  for row, line in enumerate(pipes):
    for col, c in enumerate(line):
      if c == START: return row, col
  return -1, -1

def neighbors(pipes: list[str], r: int, c: int) -> list[Point]:
  out = []
  if r and pipes[r - 1][c] in [NORTH_SOUTH, SOUTH_WEST, SOUTH_EAST]: out.append((r - 1, c))
  if r < len(pipes) - 1 and pipes[r + 1][c] in [NORTH_SOUTH, NORTH_EAST, NORTH_WEST]: out.append((r + 1, c))
  if c and pipes[r][c - 1] in [EAST_WEST, SOUTH_EAST, NORTH_EAST]: out.append((r, c - 1))
  if c < len(pipes[0]) - 1 and pipes[r][c + 1] in [EAST_WEST, NORTH_WEST, SOUTH_WEST]: out.append((r, c + 1))
  return out

def follow(pipes: list[str], r: int, c: int, visited: set[Point]) -> Point:
  pipe = pipes[r][c]
  if pipe == NORTH_SOUTH: return (r - 1, c) if (r + 1, c) in visited else (r + 1, c)
  if pipe == EAST_WEST: return (r, c - 1) if (r, c + 1) in visited else (r, c + 1)
  if pipe == NORTH_EAST: return (r - 1, c) if (r, c + 1) in visited else (r, c + 1)
  if pipe == NORTH_WEST: return (r - 1, c) if (r, c - 1) in visited else (r, c - 1)
  if pipe == SOUTH_WEST: return (r + 1, c) if (r, c - 1) in visited else (r, c - 1)
  return (r + 1, c) if (r, c + 1) in visited else (r, c + 1)


def find_path(pipes: list[str]) -> list[Point]:
  sr, sc = find_start(pipes)
  visited = set([(sr, sc)])
  path = [(sr, sc)]
  current, finish = neighbors(pipes, sr, sc)
  while current != finish:
    visited.add(current)
    path.append(current)
    current = follow(pipes, current[0], current[1], visited)
  path.append(current)
  return path


def part1(pipes: list[str]) -> int:
  path = find_path(pipes)
  return len(path) // 2

def main():
  for filename in sys.argv[1:]:
    with open(filename) as f: pipes = f.read().strip().split('\n')
    print(part1(pipes))


if __name__ == '__main__':
  main()
