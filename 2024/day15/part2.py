ROBOT = "@"
BOX = "O"
LBOX = "["
RBOX = "]"
WALL = "#"
FREE = "."
UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"

with open("input.txt") as f:
  house, moves = f.read().strip("\n").split("\n\n")

def widen(line: list[str]) -> list[str]:
  out = []
  for x in line:
    if x == FREE: out.extend([FREE, FREE])
    if x == BOX: out.extend([LBOX, RBOX])
    if x == WALL: out.extend([WALL, WALL])
    if x == ROBOT: out.extend([ROBOT, FREE])
  return out

house = [widen(list(line)) for line in house.split("\n")]

moves = moves.replace("\n", "")


r, c = None, None
found = False
for row, line in enumerate(house):
  for col, x in enumerate(line):
    if x == ROBOT: 
      r, c = row, col
      found = True
      break
  if found: break

if r is None or c is None: raise RuntimeError("No robot found")

def delta(direction):
  if direction == RIGHT: return  0, 1
  if direction == LEFT: return 0, -1
  if direction == UP: return -1, 0
  if direction == DOWN: return 1, 0
  return 0, 0


def can_move(points, direction, house):
  dr, dc = delta(direction)
  return all(house[r + dr][c + dc] != WALL for r, c in points)

def expand(points, direction, house):
  new_points = set()
  dr, dc = delta(direction)
  for r, c in points:
    new_points.add((r, c))
    if house[r + dr][c + dc] == FREE: continue
    new_points.add((r + dr, c + dc))
    if house[r + dr][c + dc] == LBOX: new_points.add((r + dr, c + dc + 1))
    if house[r + dr][c + dc] == RBOX: new_points.add((r + dr, c + dc - 1))
  return new_points, len(points) != len(new_points)

def update(house, points, direction):
  dr, dc = delta(direction)
  which = {}
  for r, c in points:
    which[(r, c)] = house[r][c]
    house[r][c] = FREE
  for r, c in points: house[r+dr][c+dc] = which[(r, c)]


for move in moves:
  # print("\n".join("".join(line) for line in house))
  # print(f"\nMove {move}")
  # print(f"robot is now a {house[r][c]}")
  points = {(r, c)}
  while can_move(points, move, house):
    points, changed = expand(points, move, house)
    if not changed: break
  if not can_move(points, move, house): continue
  update(house, points, move)
  dr, dc = delta(move)
  r, c = r + dr, c + dc

  

# print("\n".join("".join(line) for line in house))

total = 0
for r, line in enumerate(house):
  for c, x in enumerate(line):
    if x == LBOX:
      total += 100 * r + c
print(total)
