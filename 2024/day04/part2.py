with open("input.txt") as f:
  g = f.read().strip("\n").split("\n")

rows = len(g)
cols = len(g[0])


total = 0
for r in range(rows):
  for c in range(cols):
    if r in [0, rows - 1]: continue
    if c in [0, rows - 1]: continue
    if g[r][c] != "A": continue
    total += g[r-1][c-1] + g[r+1][c+1] in ["MS", "SM"] and g[r-1][c+1] + g[r+1][c-1] in ["MS", "SM"]



print(total)
