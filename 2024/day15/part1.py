ROBOT = "@"
BOX = "O"
WALL = "#"
FREE = "."
UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"

with open("input.txt") as f:
  house, moves = f.read().strip("\n").split("\n\n")

house = [list(line) for line in house.split("\n")]
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

for move in moves:
  # print("\n".join("".join(line) for line in house))
  # print(f"\nMove {move}")
  # print(f"robot is now a {house[r][c]}")
  to_move = [(r, c)]
  if move == RIGHT:
    while house[r][c + 1] == BOX:
      r, c = r, c + 1
      to_move.append((r, c))
    if house[r][c + 1] == WALL:
      r, c = to_move[0]
      continue
    while to_move:
      r, c = to_move.pop()
      house[r][c + 1] = house[r][c]
    house[r][c] = FREE
    r, c = r, c + 1

  if move == LEFT:
    while house[r][c - 1] == BOX:
      r, c = r, c - 1
      to_move.append((r, c))
    if house[r][c - 1] == WALL:
      r, c = to_move[0]
      continue
    while to_move:
      r, c = to_move.pop()
      house[r][c - 1] = house[r][c]
    house[r][c] = FREE
    r, c = r, c - 1

  if move == DOWN:
    while house[r + 1][c] == BOX:
      r, c = r + 1, c
      to_move.append((r, c))
    if house[r + 1][c] == WALL:
      r, c = to_move[0]
      continue
    while to_move:
      r, c = to_move.pop()
      house[r + 1][c] = house[r][c]
    house[r][c] = FREE
    r, c = r+1, c

  if move == UP:
    while house[r - 1][c] == BOX:
      r, c = r - 1, c
      to_move.append((r, c))
    if house[r - 1][c] == WALL:
      r, c = to_move[0]
      continue
    while to_move:
      r, c = to_move.pop()
      house[r - 1][c] = house[r][c]
    house[r][c] = FREE
    r, c = r-1, c
# print("\n".join("".join(line) for line in house))

total = 0
for r, line in enumerate(house):
  for c, x in enumerate(line):
    if x == BOX:
      total += 100 * r + c
print(total)
