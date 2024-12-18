filename = "input.txt"
with open(filename) as f:
  fall = [
      tuple([int(x) for x in line.split(",")])
      for line in f.read().strip("\n").split("\n")
  ]


length = 71 if filename == "input.txt" else 7

def can_reach(n) -> bool:
  obstacles = set(fall[:n])
  visited = set()
  frontier = [(0, 0)]
  while frontier:
    new_frontier = []
    for (col, row) in frontier:
      if col == length - 1 and row == length - 1: return True
      for pc, pr in [(col - 1, row), (col + 1, row), (col, row - 1), (col, row + 1)]:
        if pc < 0 or pc >= length: continue
        if pr < 0 or pr >= length: continue
        if (pc, pr) in obstacles: continue
        if (pc, pr) in visited: continue
        visited.add((pc, pr))
        new_frontier.append((pc, pr))
    frontier = new_frontier
  return False

# Not 282
for i in range(len(fall)):
  if not can_reach(i):
    print(fall[i-1])
    break
