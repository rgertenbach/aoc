from os import name
import re
import sys
from typing import NamedTuple, Iterable


class CompatRng(NamedTuple):
  src: int
  dst: int
  len: int
 
  # __in__ doesn't fucking work
  def has(self, dst: int) -> bool:
    return dst >= self.dst and dst < (self.dst + self.len)

  def __getitem__(self, dst: int) -> int:
    off = dst - self.dst
    return self.src + off

class Compat:
  def __init__(self, ranges: Iterable[CompatRng]):
    self.ranges = list(ranges)

  def __getitem__(self, dst: int) -> int:
    for rng in self.ranges:
      if rng.has(dst): return rng[dst]
    return dst

def parse(s: str) -> tuple[list[int], list[CompatRng]]:
    raw_seeds, *raw_maps = s.split('\n\n')
    seeds = [int(x) for x in raw_seeds.split(' ')[1:]]
    maps = []
    for raw_map in raw_maps:
      raw_ranges = raw_map.split('\n')[1:]
      maps.append([
        CompatRng(*(int(x) for x in raw_range.split(' ')))
        for raw_range in raw_ranges])
    return seeds, maps
  
def part1(seeds, maps):
  compats = [Compat(mapping) for mapping in maps]
  smallest = None
  for seed in seeds:
    x = seed
    for compat in compats:
      x = compat[x]
    if smallest is None or x < smallest: smallest = x
  return smallest
  

def main():
  for filename in sys.argv[1:]:
    with open(filename) as f: data = f.read().strip('\n')
    seeds, maps = parse(data)
    print(part1(seeds, maps))

if __name__ == '__main__':
  main()
