import math
import time
from collections import deque
from collections import namedtuple

from enum import Enum

Point = namedtuple('Point', ['x', 'y'])

START = Point(0, -1)


Vortex = namedtuple('Vortex', ['pos', 'direction'])
State = namedtuple('State', ['pos', 'cycle'])


def lcm(a, b):
  return (a * b) // math.gcd(a, b)


def load(filename: str) -> tuple[list[Vortex], int, int, Point]:
  with open(filename) as f:
    rows = f.read().strip().split('\n')

  rows = rows[1:-1]
  rows = [row.strip('#') for row in rows]
  height = len(rows)
  width = len(rows[0])
  vortexes = []
  for y, row in enumerate(rows):
    for x, direction in enumerate(row):
      if direction not in '^v<>':
        continue
      vortexes.append(Vortex(Point(x, y), direction))

  end = Point(width - 1, height)
  return vortexes, width, height, end


def state_at_cycle(
    vortex: Vortex, cycle: int, width: int, height: int) -> State:
  if vortex.direction == '^':
    return State(Point(vortex.pos.x, (vortex.pos.y - cycle) % height), cycle)
  if vortex.direction == 'v':
    return State(Point(vortex.pos.x, (vortex.pos.y + cycle) % height), cycle)
  if vortex.direction == '<':
    return State(Point((vortex.pos.x - cycle) % width, vortex.pos.y), cycle)
  if vortex.direction == '>':
    return State(Point((vortex.pos.x + cycle) % width, vortex.pos.y), cycle)
  raise RuntimeError(f'Invalid direction: {vortex.direction}')


def build_occupied_map(
    vortexes: list[Vortex], width: int, height: int) -> tuple[set[State], int]:
  out = set()
  cycles_needed = lcm(width, height)
  for cycle in range(cycles_needed):
    for vortex in vortexes:
      out.add(state_at_cycle(vortex, cycle, width, height))
  return out, cycles_needed


def propose_move(current: State, direction: str, width: int, height: int) -> State | None:
  dests = [Point(0, -1), Point(width - 1, height)]
  proposed = current.pos
  if direction == '^':
    proposed = Point(current.pos.x, current.pos.y - 1)
  elif direction == 'v':
    proposed = Point(current.pos.x, current.pos.y + 1)
  elif direction == '<':
    proposed = Point(current.pos.x - 1, current.pos.y)
  elif direction == '>':
    proposed = Point(current.pos.x + 1, current.pos.y)
  
  proposed_state = State(proposed, current.cycle + 1)
  if proposed in dests:
    return proposed_state
  if 0 <= proposed.x < width and 0 <= proposed.y < height:
    return proposed_state
  return None



def is_occ(occ: set[State], state: State, cycles: int) -> bool:
  return State(state.pos, state.cycle % cycles) in occ


def find_quickest_path(current: State,
                       dest: Point,
                       occ: set[State], 
                       width: int, 
                       height: int,
                       occ_cycles: int) -> int | float:
  pm = lambda d: propose_move(current, d, width, height)
  visited = set([current])
  proposals = deque([current])

  while proposals:
    current = proposals.popleft()

    for d in 'v>.^<':
      prop = pm(d)
      if prop is None:
        continue
      if prop.pos == dest:
        return prop.cycle
      if prop in visited:
        continue
      if is_occ(occ, prop, occ_cycles):
        continue
      proposals.append(prop)
      visited.add(prop)

  raise RuntimeError('No path found')



def quickest(filename: str) -> int | float:
  vortexes, width, height, dest = load(filename)
  occ_map, occ_cycles = build_occupied_map(vortexes, width, height)
  there = find_quickest_path(State(START, 0), dest, occ_map, width, height, occ_cycles)
  back = find_quickest_path(State(dest, there), START, occ_map, width, height, occ_cycles)
  retour = find_quickest_path(State(START, back), dest, occ_map, width, height, occ_cycles)

  return retour


def main():
  print(quickest('test_input.txt'))
  print(quickest('input.txt'))


if __name__ == '__main__':
  main()
        
# def quickest(filename: str) -> int | float:
#   vortexes, width, height, dest = load(filename)
#   occ_map, occ_cycles = build_occupied_map(vortexes, width, height)
#   quickest = find_quickest_path(State(START, 0), dest, occ_map, width, height, occ_cycles)
#   return quickest
