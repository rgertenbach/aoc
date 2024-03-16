with open('input.txt') as f:
  walls = f.read().split('\n')

def parse_wall(wall):
  return [tuple(int(x) for x in node.split(',')) for node in wall.split(' -> ')]

walls = [parse_wall(wall) for wall in walls]

emit_x = 500
floor_depth = max(y for wall in walls for z, y in wall) + 2
print(f'{floor_depth=}')


wallpts = set()

for wall in walls:
  for (sx, sy), (ex, ey) in zip(wall[:-1], wall[1:]):
    if sx == ex: # vertical
      for y in range(min(sy, ey), max(sy, ey) + 1):
        wallpts.add((sx, y))
    else:  # horizontal
      for x in range(min(sx, ex), max(sx, ex) + 1):
        wallpts.add((x, sy))

pile = set()

def fall(xy):
  x, y = xy
  for dest in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
    if (
        dest not in pile
        and dest not in wallpts
        and dest[1] < floor_depth
        and dest != (500, 0)):
      return dest
  return xy


while (500, 0) not in pile:
  flake = (emit_x, 0)
  while (dest := fall(flake)) != flake:
    flake = dest
  pile.add(flake)

print(len(pile))
