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

def circle(grid, current, block):
  grid = grid[:]
  if block is not None:
    grid[block[0]] = ''.join(("#" if i == block[1] else x) for i, x in enumerate(grid[block[0]]))
  facing = UP
  visited = set()
  while (current, facing) not in visited:
    visited.add((current, facing))
    proposed = move(current, facing)
    if proposed[0] < 0 or proposed[0] >= rows or proposed[1] < 0 or proposed[1] >= cols: return False
    while grid[proposed[0]][proposed[1]] == "#":
      facing = turn(facing)
      proposed = move(current, facing)
      if proposed[0] < 0 or proposed[0] >= rows or proposed[1] < 0 or proposed[1] >= cols: return False
    current = proposed
  return (current, facing) in visited


with open("input.txt") as f:
  grid = f.read().strip("\n").split("\n")

rows = len(grid)
cols = len(grid[0])
visited = set()

done = False

start = None
for r, row in enumerate(grid):
  for c, x in enumerate(row):
    if x == "^":
      start = (r, c)
      done = True
      break
  if done: break

current = start
if current is None: raise RuntimeError("No start found")
facing = UP
while True:
  visited.add(current)
  proposed = move(current, facing)
  if proposed[0] < 0 or proposed[0] >= rows or proposed[1] < 0 or proposed[1] >= cols: break
  while grid[proposed[0]][proposed[1]] == "#":
    facing = turn(facing)
    proposed = move(current, facing)
  current = proposed

total = 0

# remove start
for block in visited:
  total += circle(grid, start, block)

print(total)
        
      
