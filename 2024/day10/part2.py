with open("input.txt") as f:
  topo = [[*map(int, line)] for line in f.read().strip("\n").split("\n")]

total = 0

rows = len(topo)
cols = len(topo[0])
for start_row, row in enumerate(topo):
  for start_col, x in enumerate(row):
    if x != 0: continue
    frontier = [(start_row, start_col, 0)]
    score = 0
    while frontier:
      new_frontier = []
      for cr, cc, h in frontier:
        if h == 9: 
          score += 1
        if cr > 0        and topo[cr - 1][cc] == h + 1: new_frontier.append((cr - 1, cc, h + 1))
        if cr < rows - 1 and topo[cr + 1][cc] == h + 1: new_frontier.append((cr + 1, cc, h + 1))
        if cc > 0        and topo[cr][cc - 1] == h + 1: new_frontier.append((cr, cc - 1, h + 1))
        if cc < cols - 1 and topo[cr][cc + 1] == h + 1: new_frontier.append((cr, cc + 1, h + 1))
      frontier = new_frontier
    total += score


print(total)
