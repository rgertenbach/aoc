import sys
from typing import NamedTuple, Optional
from enum import Enum


class Point(NamedTuple):
  row: int
  col: int

  def move(self, direction: 'Direction') -> 'Point':
    if direction is Direction.WEST: return Point(self.row, self.col - 1)
    if direction is Direction.EAST: return Point(self.row, self.col + 1)
    if direction is Direction.NORTH: return Point(self.row - 1, self.col)
    return Point(self.row + 1, self.col)

  def heading(self, next_point: 'Point') -> 'Direction':
    dr = next_point.row - self.row 
    dc = next_point.col - self.col
    if dr == -1: return Direction.NORTH
    if dr == 1: return Direction.SOUTH
    if dc == -1: return Direction.WEST
    return Direction.EAST

class Pipe(Enum):
  NORTH_SOUTH = '|'
  EAST_WEST = '-'
  NORTH_EAST = 'L'
  NORTH_WEST = 'J'
  SOUTH_WEST = '7'
  SOUTH_EAST = 'F'
  START = 'S'
  GROUND = '.'
  OTHER = 'O'
  OTHER2 = 'I'

  @property
  def goes_north(self) -> bool:
    return self in {Pipe.NORTH_SOUTH, Pipe.NORTH_WEST, Pipe.NORTH_EAST}

  @property
  def goes_south(self) -> bool:
    return self in {Pipe.NORTH_SOUTH, Pipe.SOUTH_WEST, Pipe.SOUTH_EAST}

  @property
  def goes_west(self) -> bool:
    return self in {Pipe.EAST_WEST, Pipe.SOUTH_WEST, Pipe.NORTH_WEST}

  @property
  def goes_east(self) -> bool:
    return self in {Pipe.EAST_WEST, Pipe.NORTH_EAST, Pipe.SOUTH_EAST}

  @property
  def turns(self) -> bool:
    return self in {
        Pipe.NORTH_WEST, Pipe.NORTH_EAST, Pipe.SOUTH_WEST, Pipe.SOUTH_EAST}

  def direction_of_turn(self, direction: 'Direction') -> 'Turn':
      if self is Pipe.NORTH_WEST:
        return Turn.CLOCK if direction is Direction.WEST else Turn.COUNTER
      if self is Pipe.NORTH_EAST:
        return Turn.CLOCK if direction is Direction.NORTH else Turn.COUNTER
      if self is Pipe.SOUTH_WEST:
        return Turn.CLOCK if direction is Direction.SOUTH else Turn.COUNTER
      # SOUTH_EAST
      return Turn.CLOCK if direction is Direction.EAST else Turn.COUNTER

  @classmethod
  def from_directions(cls, came: 'Direction', goes: 'Direction') -> 'Pipe':
    if came is Direction.EAST and goes is Direction.NORTH: return Pipe.NORTH_WEST
    if came is Direction.SOUTH and goes is Direction.WEST: return Pipe.NORTH_WEST
    if came is Direction.EAST and goes is Direction.SOUTH: return Pipe.SOUTH_WEST
    if came is Direction.NORTH and goes is Direction.WEST: return Pipe.SOUTH_WEST
    if came is Direction.WEST and goes is Direction.NORTH: return Pipe.NORTH_EAST
    if came is Direction.SOUTH and goes is Direction.EAST: return Pipe.NORTH_EAST
    if came is Direction.WEST and goes is Direction.SOUTH: return Pipe.SOUTH_EAST
    if came is Direction.NORTH and goes is Direction.EAST: return Pipe.SOUTH_EAST

    if came is Direction.SOUTH and goes is Direction.SOUTH: return Pipe.NORTH_SOUTH
    if came is Direction.NORTH and goes is Direction.NORTH: return Pipe.NORTH_SOUTH
    if came is Direction.WEST and goes is Direction.WEST: return Pipe.EAST_WEST
    if came is Direction.EAST and goes is Direction.EAST: return Pipe.EAST_WEST
    raise RuntimeError(f'{came} -> {goes} not supported')

class Pipes:
  def __init__(self, pipes: list[list[Pipe]]):
    self.pipes = pipes

  def __getitem__(self, point: Point) -> Pipe:
    return self.pipes[point.row][point.col]

  def find_start(self) -> Point:
    for row, line in enumerate(self.pipes):
      for col, pipe in enumerate(line):
        if pipe is Pipe.START: return Point(row, col)
    raise RuntimeError('No start found')

  @property
  def rows(self): return len(self.pipes)

  @property
  def cols(self): return len(self.pipes[0])

  def print(self, outside: set[Point], path: set[Point], current: Point | None = None, out_dir: Optional['Direction'] = None) -> None:

    for row, line in enumerate(self.pipes):
      for col, pipe in enumerate(line):
        point = Point(row, col)
        pipe = self[point]
        if current is not None and point == current: 
          if out_dir is None: print('@', end='')
          elif out_dir is Direction.NORTH: print('🢁', end='')
          elif out_dir is Direction.SOUTH: print('🢃', end='')
          elif out_dir is Direction.WEST: print('🢀', end='')
          else: print('🢂', end='')
        elif point in path: 
          if pipe is Pipe.NORTH_SOUTH: print('│', end='')
          if pipe is Pipe.NORTH_WEST: print('┘', end='')
          if pipe is Pipe.NORTH_EAST: print('└', end='')
          if pipe is Pipe.EAST_WEST: print('─', end='')
          if pipe is Pipe.SOUTH_WEST: print('┐', end='')
          if pipe is Pipe.SOUTH_EAST: print('┌', end='')
          if pipe is Pipe.START: print('S', end='')
        elif point in outside: print('~', end='')
        else: print(pipe.value, end='')
      print()


class Direction(Enum):
  NORTH = 1
  SOUTH = 2
  WEST = 3
  EAST = 4

  def turn(self, wise: 'Turn') -> 'Direction':
    if self is Direction.NORTH:
      return Direction.WEST if wise is Turn.COUNTER else Direction.EAST
    if self is Direction.SOUTH:
      return Direction.EAST if wise is Turn.COUNTER else Direction.WEST
    if self is Direction.WEST:
      return Direction.SOUTH if wise is Turn.COUNTER else Direction.NORTH
    # East
    return Direction.NORTH if wise is Turn.COUNTER else Direction.SOUTH

class Turn(Enum):
  CLOCK = 'clock'
  COUNTER = 'counter'

def neighbors(pipes: Pipes, point: Point) -> list[Point]:
  r, c = point
  out = []
  if r and pipes[point.move(Direction.NORTH)].goes_south:
    out.append(point.move(Direction.NORTH))
  if r < pipes.rows - 1 and pipes[point.move(Direction.SOUTH)].goes_north:
    out.append(point.move(Direction.SOUTH))
  if c and pipes[point.move(Direction.WEST)].goes_east:
    out.append(point.move(Direction.WEST))
  if c < pipes.cols - 1 and pipes[point.move(Direction.EAST)].goes_west:
    out.append(point.move(Direction.EAST))
  return out

def follow(pipes: Pipes, current: Point, visited: set[Point]) -> Point:
  pipe = pipes[current]
  north = current.move(Direction.NORTH)
  south = current.move(Direction.SOUTH)
  west = current.move(Direction.WEST)
  east = current.move(Direction.EAST)
  if pipe is Pipe.NORTH_SOUTH: return north if south in visited else south
  if pipe is Pipe.EAST_WEST: return west if east in visited else east
  if pipe is Pipe.NORTH_EAST: return north if east in visited else east
  if pipe is Pipe.NORTH_WEST: return north if west in visited else west
  if pipe is Pipe.SOUTH_WEST: return south if west in visited else west
  # South east
  return south if east in visited else east

def find_path(pipes: Pipes) -> list[Point]:
  start = pipes.find_start()
  visited: set[Point] = set([start])
  path = [start]
  current, finish = neighbors(pipes, start)
  while current != finish:
    visited.add(current)
    path.append(current)
    current = follow(pipes, current, visited)
  path.append(current)
  return path

def flood_fill(outside: set[Point], pipes: Pipes, point: Point, boundary: set[Point]) -> None:
  points = [point]
  while points:
    point = points.pop()
    outside.add(point)
    if point.col and (prop := point.move(Direction.WEST)) not in boundary and prop not in outside:
      points.append(prop)
    if point.col < pipes.cols - 1 and (prop := point.move(Direction.EAST)) not in boundary and prop not in outside:
      points.append(prop)
    if point.row and (prop := point.move(Direction.NORTH)) not in boundary and prop not in outside:
      points.append(prop)
    if point.row < pipes.rows - 1 and (prop := point.move(Direction.SOUTH)) not in boundary and prop not in outside:
      points.append(prop)

def enclosed_area(pipes: Pipes, path: list[Point]) -> int:
  boundary = set(path)
  outside = set()

  # flood fill outside
  for c in range(pipes.cols):
    if (0, c) not in boundary:
      flood_fill(outside, pipes, Point(0, c), boundary)
    if (pipes.rows - 1, c) not in boundary:
      flood_fill(outside, pipes, Point(pipes.rows - 1, c), boundary)
  for r in range(1, pipes.rows - 1):
    if (r, 0) not in boundary:
      flood_fill(outside, pipes, Point(r, 0), boundary)
    if (r, pipes.cols - 1) not in boundary:
      flood_fill(outside, pipes, Point(r, pipes.cols - 1), boundary)

  # Now to account for squeezing we walk along the boundary keeping track of
  # what direction outside should be!

  dir_out = Direction.NORTH
  start = 0

  # First find a good start
  for start, point in enumerate(path):
    if pipes[point] is not Pipe.NORTH_SOUTH: continue
    if point.col and point.move(Direction.WEST) in outside:
      dir_out = Direction.WEST
      break
    if point.col < pipes.cols - 1 and point.move(Direction.EAST) in outside:
      dir_out = Direction.EAST
      break

  # Now we walk along and do flood fill along the way.
  # Remember to mind the S case
  path = path[start:] + path[:start]
  for i, point in enumerate(path):
    # First we flood fill looking into the right direction if it's not in the path or outside
    prop = point.move(dir_out)
    if (
        (
          (dir_out is Direction.NORTH and point.row)
          or (dir_out is Direction.SOUTH and point.row < pipes.rows - 1)
          or (dir_out is Direction.WEST and point.col)
          or (dir_out is Direction.EAST and point.col < pipes.cols - 1))
        and prop not in boundary
        and prop not in outside):
      flood_fill(outside, pipes, prop, boundary)


    pipe = pipes[point]
    next_point = path[i + 1] if i < len(path) - 1 else path[0]
    direction_of_travel = point.heading(next_point)
    if pipe is Pipe.START:
      prev_point = path[i - 1] if i else path[-1]
      prev_direction_of_travel = prev_point.heading(point)
      pipe = Pipe.from_directions(prev_direction_of_travel, direction_of_travel)

    if pipe.turns:
      dir_out = dir_out.turn(pipe.direction_of_turn(direction_of_travel))

      prop = point.move(dir_out)
      if (
          (
            (dir_out is Direction.NORTH and point.row)
            or (dir_out is Direction.SOUTH and point.row < pipes.rows - 1)
            or (dir_out is Direction.WEST and point.col)
            or (dir_out is Direction.EAST and point.col < pipes.cols - 1))
          and prop not in boundary
          and prop not in outside):
        flood_fill(outside, pipes, prop, boundary)


  #356 too high
  return pipes.rows * pipes.cols - len(boundary.union(outside))

def main():
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f:
      pipes = Pipes([[Pipe(x) for x in row] for row in f.read().strip().split('\n')])
    path = find_path(pipes)
    print('  Part 1:', len(path) // 2)
    if filename == 'test4.txt': print('  Should be 4')
    if filename == 'test3.txt': print('  Should be 8')
    if filename == 'test2.txt': print('  Should be 10')
    print('  Part 2:', enclosed_area(pipes, path))


if __name__ == '__main__':
  main()

