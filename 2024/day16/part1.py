import heapq
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

def fmaze(maze: list[list[str]]) -> str:
  return "\n".join("".join(line) for line in maze)

with open("input.txt") as f:
  maze = [list(line) for line in f.read().strip("\n").split("\n")]

sr, sc = None, None
er, ec = None, None


for row, line in enumerate(maze):
  for col, x in enumerate(line):
    if x == "S": sr, sc = row, col
    elif x == "E": er, ec = row, col

if sr is None: raise ValueError("sr not found")
if sc is None: raise ValueError("sc not found")
if er is None: raise ValueError("er not found")
if ec is None: raise ValueError("ec not found")

cost = None
queue = [(0, sr, sc, EAST)]
visited = set()
while queue:
  cost, r, c, face = heapq.heappop(queue)
  if (r, c) in visited: continue
  visited.add((r, c))
  if (r, c) == (er, ec): break

  pr, pc = move(r, c, face)
  if maze[pr][pc] != WALL : heapq.heappush(queue, (cost + 1, pr, pc, face))
  pf = TURN_CLOCKWISE[face]
  pr, pc = move(r, c, pf)
  if maze[pr][pc] != WALL: heapq.heappush(queue, (cost + 1001, pr, pc, pf))
  pf = TURN_COUNTERCLOCKWISE[face]
  pr, pc = move(r, c, pf)
  if maze[pr][pc] != WALL: heapq.heappush(queue, (cost + 1001, pr, pc, pf))


print(cost)

