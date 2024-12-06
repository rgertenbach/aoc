UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

def turn(facing):
  if facing == UP: return RIGHT
  if facing == RIGHT: return DOWN
  if facing == DOWN: return LEFT
  if facing == LEFT: return UP

def move(current, facing):
  if facing == UP: return current[0] - 1, current[1]
  if facing == RIGHT: return current[0], current[1] + 1
  if facing == DOWN: return current[0] + 1, current[1]
  return current[0], current[1] - 1

with open("input.txt") as f:
  grid = f.read().strip("\n").split("\n")

rows = len(grid)
cols = len(grid[0])
visited = set()

done = False
current = None
for r, row in enumerate(grid):
  for c, x in enumerate(row):
    if x == "^":
      current = (r, c)
      done = True
      break
  if done: break

if current is None: raise RuntimeError("No start found")
facing = UP
print(f"{current=}")
while True:
  visited.add(current)
  proposed = move(current, facing)
  if proposed[0] < 0 or proposed[0] >= rows or proposed[1] < 0 or proposed[1] >= cols: break
  while grid[proposed[0]][proposed[1]] == "#":
    facing = turn(facing)
    proposed = move(current, facing)
  current = proposed

print(len(visited))
        
