with open("input.txt") as f:
  g = f.read().strip("\n").split("\n")

rows = len(g)
cols = len(g[0])

TARGET = ["XMAS", "SAMX"]

total = 0
for r in range(rows):
  for c in range(cols):
    if c <= cols - 4:
      total += g[r+0][c+0] + g[r+0][c+1] + g[r+0][c+2] + g[r+0][c+3] in TARGET
    if r <= rows - 4:
      total += g[r+0][c+0] + g[r+1][c+0] + g[r+2][c+0] + g[r+3][c+0] in TARGET
    if r <= rows - 4 and c <= cols - 4:
      total += g[r+0][c+0] + g[r+1][c+1] + g[r+2][c+2] + g[r+3][c+3] in TARGET
    if r >= 3 and c <= cols - 4:
      total += g[r-0][c+0] + g[r-1][c+1] + g[r-2][c+2] + g[r-3][c+3] in TARGET


print(total)
