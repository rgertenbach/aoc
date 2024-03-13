import sys
import lib



def part1(hail: list[lib.Stone]) -> int:
  LOWER = 200000000000000
  UPPER = 400000000000000
  cnt = 0
  for off, stone in enumerate(hail):
    for other in hail[off + 1:]:
      intersection = stone.intersects_xy(other)
      if intersection is None: continue
      print(f'{stone} and {other} intersect at {intersection}')
      int_x, int_y, _ = intersection
      if LOWER <= int_x <= UPPER and LOWER <= int_y <= UPPER:
        cnt += 1
        print('Thats in')
  return cnt

def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f:
      hail = [lib.Stone.parse(x) for x in f.read().strip().split('\n')]
    print(part1(hail))
    # 18718 is wrong

if __name__ == '__main__':
  main()
