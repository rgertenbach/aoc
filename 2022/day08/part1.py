with open('input.txt') as f:
  heights = [row.strip() for row in f.readlines()]


nrows = len(heights)
ncols = len(heights[0])
vis = 0

for rowi in range(nrows):
  for coli in range(ncols):
    if rowi in (0, nrows - 1) or coli in (0, ncols - 1):
      vis += 1
      continue

    above = max(row[coli] for row in heights[:rowi])
    below = max(row[coli] for row in heights[rowi + 1:])
    left =  max(heights[rowi][:coli])
    right = max(heights[rowi][coli + 1:])
    if min(above, below, left, right) < heights[rowi][coli]:
      vis += 1

print(vis)



