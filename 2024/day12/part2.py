with open("test_input.txt") as f:
  garden = f.read().strip("\n").split("\n")

processed = set()
plots: list[set[tuple[int, int]]] = []

rows = len(garden)
cols = len(garden[0])

def sides(plot: set[tuple[int, int]]):
  out = 0
  # Top edges
  processed = set()
  for row, col in plot:
    if (row, col) in processed: continue
    processed.add((row, col))
    if (row - 1, col) in plot: continue
    out += 1
    right = col + 1
    while (row, right) in plot and (row - 1, right) not in plot:
      processed.add((row, right))
      right += 1
    right = col - 1
    while (row, right) in plot and (row - 1, right) not in plot:
      processed.add((row, right))
      right -= 1
  # Bottom edges
  processed = set()
  for row, col in plot:
    if (row, col) in processed: continue
    processed.add((row, col))
    if (row + 1, col) in plot: continue
    out += 1
    right = col + 1
    while (row, right) in plot and (row + 1, right) not in plot:
      processed.add((row, right))
      right += 1
    right = col - 1
    while (row, right) in plot and (row + 1, right) not in plot:
      processed.add((row, right))
      right -= 1
  # Left edges
  processed = set()
  for row, col in plot:
    if (row, col) in processed: continue
    processed.add((row, col))
    if (row, col - 1) in plot: continue
    out += 1
    down = row + 1
    while (down, col) in plot and (down, col - 1) not in plot:
      processed.add((down, col))
      down += 1
    down = row - 1
    while (down, col) in plot and (down, col - 1) not in plot:
      processed.add((down, col))
      down -= 1
  # Right edges
  processed = set()
  for row, col in plot:
    if (row, col) in processed: continue
    processed.add((row, col))
    if (row, col + 1) in plot: continue
    out += 1
    down = row + 1
    while (down, col) in plot and (down, col + 1) not in plot:
      processed.add((down, col))
      down += 1
    down = row - 1
    while (down, col) in plot and (down, col + 1) not in plot:
      processed.add((down, col))
      down -= 1

  return out



for row, line in enumerate(garden):
  for col, x in enumerate(line):
    if (row, col) in processed: continue
    processed.add((row, col))
    plot = set()
    stack = [(row, col)]
    while stack:
      r, c = stack.pop()
      plot.add((r, c))
      if r > 0 and garden[r - 1][c] == x and (r - 1, c) not in processed: 
        processed.add((r - 1, c))
        stack.append((r -  1, c))
      if r < rows - 1 and garden[r + 1][c] == x and (r + 1, c) not in processed: 
        processed.add((r + 1, c))
        stack.append((r + 1, c))
      if c > 0 and garden[r][c - 1] == x and (r, c - 1) not in processed: 
        processed.add((r, c - 1))
        stack.append((r, c - 1))
      if c < cols - 1 and garden[r][c + 1] == x and (r, c + 1) not in processed: 
        processed.add((r, c + 1))
        stack.append((r, c + 1))
    plots.append(plot)

total = 0
for plot in plots:
  area = len(plot)
  circ = sides(plot)
  total += area * circ

print(total)

