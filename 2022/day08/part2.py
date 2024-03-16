with open('input.txt') as f:
  heights = [
      [int(height) for height in row.strip()]
      for row 
      in f.readlines()]


def v(height, trees):
  visible = 0
  for tree in trees:
    visible += 1
    if tree >= height:
      break
  return visible


nrows = len(heights)
ncols = len(heights[0])
best = 0

for rowi in range(1, nrows - 1):
  row = heights[rowi]
  for coli in range(1, ncols - 1):
    col = [row[coli] for row in heights]
    height = row[coli]

    above = v(height, reversed(col[:rowi]))  # above
    below = v(height, col[rowi + 1:])      # below
    right = v(height, reversed(row[:coli]))  # left
    left = v(height, row[coli + 1:])      # right
    vis = above * below * left * right
    if vis > best:
      best = vis


print(best)
