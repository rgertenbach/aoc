import sys
sys.path.append('.')
import shapes


def fall(bricks: list[shapes.Brick]) -> None:
  for i, brick in enumerate(bricks):
    bricks_below = [b for b in bricks[:i] if b.highest_point < brick.lowest_point]
    bricks_below = [b for b in bricks_below if brick.is_above(b)]
    # print(f'{bricks_below} are below {brick}')
    if bricks_below:
      support = max(bricks_below, key=lambda b: b.highest_point).highest_point
    else:
      support = 0
    drop_amt = brick.lowest_point - support - 1
    brick.drop(drop_amt)

def bricks_just_above(bricks: list[shapes.Brick]) -> list[list[shapes.Brick]]:
  out = []
  for i, brick in enumerate(bricks):
    bricks_above = [b for b in bricks[i+1:] if b.lowest_point - brick.highest_point == 1]
    bricks_above = [b for b in bricks_above if b.is_above(brick)]
    out.append(bricks_above)
  return out

def bricks_just_below(bricks: list[shapes.Brick]) -> list[list[shapes.Brick]]:
  out = []
  for i, brick in enumerate(bricks):
    bricks_below = [b for b in bricks[:i] if brick.lowest_point - b.highest_point == 1]
    bricks_below = [b for b in bricks_below if brick.is_above(b)]
    out.append(bricks_below)
  return out


def part1(bricks: list[shapes.Brick]) -> int:
  bricks = sorted(bricks, key=lambda b: b.lowest_point)
  fall(bricks)
  idx = {id(b): i for i, b in enumerate(bricks)}
  just_above = bricks_just_above(bricks)
  just_below = bricks_just_below(bricks)
  safe = 0
  for above in just_above:
    if all(len(just_below[idx[id(a)]]) > 1 for a in above):
      safe += 1


  return safe
  

def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: bricks = [shapes.Brick.parse(s) for s in f.read().strip().split('\n')]
    print(part1(bricks))
    for brick in bricks:
      if brick.p2.x > brick.p2.x: print(brick)
      if brick.p2.y > brick.p2.y: print(brick)
      if brick.p2.z > brick.p2.z: print(brick)


if __name__ == '__main__':
  main()
