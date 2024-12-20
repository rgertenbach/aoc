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

time_to_goal = {}

steps = 0
r, c = er, ec
while True:
  time_to_goal[(r, c)] = steps
  if (r, c) == (sr, sc): break
  for pr, pc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
    if track[pr][pc] == WALL or (pr, pc) in time_to_goal: continue
    r, c = pr, pc
    break
  steps += 1

def circle(r, c):
  for l1 in range(2, 21):
    for ro in range(-l1, l1+1):
      pr = r + ro
      if pr < 0 or pr >= rows: continue
      remaining_offset = l1 - abs(ro)
      for co in {-remaining_offset, remaining_offset}:
        pc = c + co
        if pc >= 0 and pc < cols and track[pr][pc] != WALL: yield pr, pc, l1


baseline = time_to_goal[(sr, sc)]
max_steps = baseline - 50
r, c = sr, sc
visited = set([(sr, sc)])
steps = 0
fast = 0
while steps <= max_steps and (r, c) != (er, ec):
  # Jumps
  for pr, pc, jump in circle(r, c):
    time = steps + jump + time_to_goal[(pr, pc)] 
    saved = baseline - time
    if saved >= 100: fast += 1
  # Moving normally
  for pr, pc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
    if track[pr][pc] == WALL or (pr, pc) in visited: continue
    r, c = pr, pc
    visited.add((pr, pc))
    break
  steps += 1


print(fast)

