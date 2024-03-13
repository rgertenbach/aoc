import sys
sys.path.append('.')
import shapes
from functools import cache


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

def part1(bricks: list[shapes.Brick], just_above: list[list[shapes.Brick]], just_below: list[list[shapes.Brick]], idx: dict[int, int]) -> int:
  return sum(all(len(just_below[idx[id(a)]]) > 1 for a in above) for above in just_above)


def break_up(brick: int, aboves: list[set[int]], belows: list[set[int]]) -> int:
  broken = {brick}
  above = aboves[brick]
  while above:
    next_above = set()
    for a in above:
      if not belows[a].difference(broken):
        broken.add(a)
        next_above.update(aboves[a])
    above = next_above
  return len(broken)


# THe issue here is that i'm not considering what;s broken
# if A breaks B and C and D rests on B and C it currently doesn't break when it should!
def part2(just_above: list[list[shapes.Brick]], just_below: list[list[shapes.Brick]], idx: dict[int, int]) -> int:
  bricks = list(range(len(just_above)))
  belows = [{idx[id(a)] for a in above} for above in just_below]
  aboves = [{idx[id(a)] for a in above} for above in just_above]  # At most 409 above
  total = 0
  for brick in range(len(just_above)): total += break_up(brick, aboves, belows)
  return total - len(bricks)
  

def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: bricks = [shapes.Brick.parse(s) for s in f.read().strip().split('\n')]
    bricks = sorted(bricks, key=lambda b: b.lowest_point)
    fall(bricks)
    idx = {id(b): i for i, b in enumerate(bricks)}
    just_above = bricks_just_above(bricks)
    just_below = bricks_just_below(bricks)
    print(part1(bricks, just_above, just_below, idx))
    print(part2(just_above, just_below, idx))

if __name__ == '__main__':
  main()
