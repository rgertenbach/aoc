import re
import sys
from typing import NamedTuple
from math import prod

class Race(NamedTuple):
  time: int
  best: int


def ways_to_beat(race: Race) -> int:
  time, best = race
  # x * (time - x) > best
  # x * time - x * x > best
  # -x**2 + x * time > best
  # beat = 0
  # for pressed in range(1, time):
  #   dist = pressed * (time - pressed)
  #   if dist > best: beat += 1
  return 2

  # return beat


def parse1(s: str) -> list[Race]:
  times_raw, dists_raw = s.split('\n')
  times_raw = re.sub('^Time: +', '', times_raw)
  dists_raw = re.sub('^Distance: +', '', dists_raw)
  times = list(map(int, re.split(' +', times_raw)),)
  dists = list(map(int, re.split(' +', dists_raw)))
  return  list(Race(*x) for x in zip(times, dists))


def parse2(s: str) -> Race:
  times_raw, dists_raw = s.split('\n')
  times_raw = re.sub('^Time: +', '', times_raw)
  dists_raw = re.sub('^Distance: +', '', dists_raw)

  time = int(re.sub(' ', '', times_raw))
  dist = int(re.sub(' ', '', dists_raw))
  return Race(time, dist)


def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f:
      data = f.read().strip()
    print(prod(ways_to_beat(race) for race in parse1(data)))
    print(ways_to_beat(parse2(data)))
    print()


if __name__ == '__main__':
  main()
