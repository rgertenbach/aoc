import sys
sys.path.append('.')
import geoms

def extract_rectangle(paths: list[geoms.Line]) -> tuple[geoms.Rectangle, int, geoms.Point, geoms.Point]:
  l1 = paths.pop()  # last one
  l2 = paths.pop()
  l3 = paths.pop()
  row, col = 0, 0
  if l1.direction is geoms.Direction.UP:
    row = max(l1.p2.row, l3.p1.row)
    col = l1.p1.col
    p1, p2 = geoms.Point(row, l3.p1.col), geoms.Point(row, l1.p2.col)
  elif l1.direction is geoms.Direction.DOWN:
    row = min(l1.p2.row, l3.p1.row)
    col = l1.p1.col
    p1, p2 = geoms.Point(row, l3.p1.col), geoms.Point(row, l1.p2.col)
  elif l1.direction is geoms.Direction.LEFT:
    row = l1.p1.row
    col = max(l1.p2.col, l3.p1.col)
    p1, p2 = geoms.Point(l3.p1.row, col), geoms.Point(l1.p2.row, col)
  elif l1.direction is geoms.Direction.RIGHT:
    row = l1.p1.row
    col = min(l1.p2.col, l3.p1.col)
    p1, p2 = geoms.Point(l3.p1.row, col), geoms.Point(l1.p2.row, col)

  top_left = geoms.Point(min(l2.p1.row, row), min(l2. p1.col, col))
  bottom_right = geoms.Point(max(l2.p1.row, row), max(l2. p1.col, col))
  rect = geoms.Rectangle(top_left, bottom_right)

  return rect, rect.area - len(geoms.Line(p1, p2)), p1, p2


def dedupe(path: list[geoms.Point]) -> list[geoms.Point]:
  # print(f'  Before deuping: {path}')
  out = [path[0], path[1]]
  for p in path[2:]:
    if (
        geoms.Line(out[-2], out[-1]).direction is geoms.Line(out[-1], p).direction
        or out[-1] == p):
      out.pop() # print(f'  Removing {out.pop()}')
    out.append(p)
  return out


def contains(rect, points):
  for p in points:
    if p.row < rect.p1.row: continue
    if p.row > rect.p2.row: continue
    if p.col < rect.p1.col: continue
    if p.col > rect.p2.col: continue
    #print(f'{p} contained in {rect}')
    return True
  return False


def area(path: list[geoms.Point]) -> int:
  total = 0
  #print(f'{path}')
  while path:
    length_at_beginning = len(path)
    for i, (p1, p2, p3, p4) in enumerate(zip(path[:-3], path[1: -2], path[2:-1], path[3:])):
      l1, l2, l3 = geoms.Line(p1, p2), geoms.Line(p2, p3), geoms.Line(p3, p4)
      if (
          l1.direction.turns(l2.direction) is geoms.Turn.RIGHT
          and l2.direction.turns(l3.direction) is geoms.Turn.RIGHT):
        rect, a, np1, np2 = extract_rectangle([l1, l2, l3])
        prev_path = path[:i+1]
        post_path = path[i + 3:]
        if contains(rect, prev_path[:-1] + post_path[1:]):
          #print(f'contained at {len(path)}')
          continue
        #print(f'Adding {a} from {rect} with base area {rect.area}')
        total += a
        path = prev_path + [np1, np2] + post_path
        break
    path = dedupe(path)
    if len(path) == length_at_beginning: break

  print(path)
  if len(path) == 5:
    total += geoms.Rectangle(path[0], path[2]).area
  else:
    total += geoms.Rectangle(path[0], path[2]).area - len(geoms.Line(path[0], geoms.Point(path[2].row, 0)))
    total += geoms.Rectangle(path[4], geoms.Point(path[2].row, 0)).area
  return total


def part1(dig_plan: list[geoms.Dig]) -> int:
  point = geoms.Point(0, 0)
  path: list[geoms.Point] = [point]

  for dig in dig_plan:
    point = point.move(dig.dir, dig.amt)
    path.append(point)
  return area(path)


def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: data = f.read().strip().split('\n')
    dig_plan = [geoms.Dig.parse(dig) for dig in data]
    print(part1(dig_plan))
    # 40337743397556 too low
    # 40343619199143 wrong
    # 40345585494850 too high
    print(part1([d.proper() for d in dig_plan]))

if __name__ == '__main__':
  main()
