import sys
sys.path.append('.')
import geoms2 as geoms
import math


def dig(dig_plan: list[geoms.Dig]) -> list[geoms.Point]:
  current = geoms.Point(0, 0)
  out = [current]
  for dig in dig_plan:
    current.move(dig.dir, dig.amt)
    out.append(current)
  return out


def part1(dig_plan: list[geoms.Dig]) -> int:
  points = dig(dig_plan)
  print(points)


def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: data = f.read().strip().split('\n')
    dig_plan = [geoms.Dig.parse(dig) for dig in data]
    print(part1(dig_plan))
    #print(part1([d.proper() for d in dig_plan]))

if __name__ == '__main__':
  main()
