WALL = "#"
with open("input.txt") as f:
  track = f.read().strip("\n").split("\n")

sr, sc = None, None
er, ec = None, None
rows = len(track)
cols = len(track[0])

for row, line in enumerate(track):
  for col, x in enumerate(line):
    if x == "S": sr, sc = row, col
    elif x == "E": er, ec = row, col
if sr is None: raise RuntimeError("No start or end found")
if sc is None: raise RuntimeError("No start or end found")
if er is None: raise RuntimeError("No start or end found")
if ec is None: raise RuntimeError("No start or end found")

def time(cheat: tuple[int, int]) -> int:
  steps = 0
  frontier: list[tuple[int, int]] = [(sr, sc)]  # type: ignore
  visited = set([(sr, sc)])
  while frontier:
    next_frontier = []
    for r, c in frontier:
      if (r, c) == (er, ec): return steps
      for pr, pc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
        if pr < 0 or pr > rows - 1: continue
        if pc < 0 or pc > cols - 1: continue
        if track[pr][pc] == WALL and (pr, pc) != cheat: continue
        if (pr, pc) in visited: continue
        next_frontier.append((pr, pc))
        visited.add((pr, pc))
    frontier = next_frontier
    steps += 1
  return -1


hundred = 0
normal = time((0, 0))

for row, line in enumerate(track):
  for col, x in enumerate(line):
    if x != WALL: continue
    if col < cols and normal - time((row, col)) >= 100: hundred += 1

print(hundred)
