with open('input.txt') as f:
  walls = f.read().split('\n')

def parse_wall(wall):
  return [tuple(int(x) for x in node.split(',')) for node in wall.split(' -> ')]

walls = [parse_wall(wall) for wall in walls]

emit_x = 500
void_depth = max(y for wall in walls for z, y in wall) + 1

pile = set()
wallpts = set()


for wall in walls:
  for (sx, sy), (ex, ey) in zip(wall[:-1], wall[1:]):
    if sx == ex: # vertical
      for y in range(min(sy, ey), max(sy, ey) + 1):
        wallpts.add((sx, y))
    else:  # horizontal
      for x in range(min(sx, ex), max(sx, ex) + 1):
        wallpts.add((x, sy))

def fall(xy):
  x, y = xy
  for dest in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
    if dest not in pile and dest not in wallpts:
      return dest
  return xy

reached_void = False

while not reached_void:
  flake = (emit_x, 0)
  while (dest := fall(flake)) != flake and not reached_void:
    if dest[1] >= void_depth:
      reached_void = True

    flake = dest
  if not reached_void:
    pile.add(flake)

print(len(pile))
