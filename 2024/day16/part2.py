import heapq
import math
WALL = "#"
EAST = 0
WEST = 1
NORTH = 2
SOUTH = 3
CLOCKWISE = 4
COUNTERCLOCKWISE = 5

TURN_CLOCKWISE = { EAST: SOUTH, SOUTH: WEST, WEST: NORTH, NORTH: EAST }
TURN_COUNTERCLOCKWISE = { EAST: NORTH, NORTH: WEST, WEST: SOUTH, SOUTH: EAST }

def move(r, c, face):
  if face == NORTH: r -= 1
  elif face == SOUTH: r += 1
  if face == WEST: c -= 1
  elif face == EAST: c += 1
  return r, c

with open("input.txt") as f:
  maze = [list(line) for line in f.read().strip("\n").split("\n")]

sr, sc = len(maze) - 2, 1
er, ec = 1, len(maze[0]) - 2

cheapest_for_spot = {(sr, sc, EAST): 0}
cheapest_paths = set()
queue = [(0, sr, sc, EAST, set([(sr, sc)]))]
last = len(cheapest_for_spot)
total = sum(x != WALL for line in maze for x in line)

while queue:
  if len(cheapest_for_spot) > last:
    last = len(cheapest_for_spot)
    print(f"{last} / {total * 4}")
  cost, r, c, face, visited = heapq.heappop(queue)
  if (r, c, face) not in cheapest_for_spot or cost < cheapest_for_spot[(r, c, face)]: cheapest_for_spot[(r, c, face)] = cost
  if cost > cheapest_for_spot[(r, c, face)]: continue
  if cost > cheapest_for_spot.get((er, ec, face), math.inf): continue
  if (r, c) == (er, ec): 
    cheapest_paths |= visited
    continue
  pr, pc = move(r, c, face)
  if maze[pr][pc] != WALL and (pr, pc) not in visited:
    heapq.heappush(queue, (cost + 1, pr, pc, face, visited.copy() | {(pr, pc)}))
  pf = TURN_CLOCKWISE[face]
  pr, pc = move(r, c, pf)
  if maze[pr][pc] != WALL and (pr, pc) not in visited:
    heapq.heappush(queue, (cost + 1001, pr, pc, pf, visited.copy() | {(pr, pc)}))

  pf = TURN_COUNTERCLOCKWISE[face]
  pr, pc = move(r, c, pf)
  if maze[pr][pc] != WALL and (pr, pc) not in visited:
    heapq.heappush(queue, (cost + 1001, pr, pc, pf, visited.copy() | {(pr, pc)}))


print(len(cheapest_paths))
# print(cheapest_paths)

def fmaze(maze: list[list[str]], efficient) -> str:
  lines = [
      "".join([("O" if (r, c) in efficient else x) for c, x in enumerate(line)])
      for r, line in enumerate(maze)
  ]
  return "\n".join(lines)

# print(fmaze(maze, cheapest_paths))

