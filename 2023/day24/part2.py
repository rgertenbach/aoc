import sys
import lib
from collections import defaultdict
import numpy as np

def part2(hail: list[lib.Stone]) -> int:
  stone1 = hail[0]
  # need proper center, intersection of stone 1 and 2
  center = stone1.pos
  stone2 = hail[1]
  stone3 = hail[3]
  intersection1 = np.array(center) + np.linalg.solve(
      np.array([-(stone3.speed), stone1.speed, (stone2.speed)]).T,
      stone3.pos-center)
  print(f'intersection1 at {intersection1}')


def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f:
      hail = [lib.Stone.parse(x) for x in f.read().strip().split('\n')]
    print(part2(hail))

if __name__ == '__main__':
  main()
