import sys
import itertools
from typing import NamedTuple, Iterable, Iterator

class SeedRng(NamedTuple):
  start: int
  len: int

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

  def supports(self, dsts: SeedRng) -> int:
    if not self.has(dsts.start): return 0
    limit = self.dst + self.len
    smallest_impossible = min(limit, dsts.start + dsts.len)
    return smallest_impossible - dsts.start

class Compat:
  def __init__(self, ranges: Iterable[CompatRng]):
    self.ranges = sorted(list(ranges), key=lambda x: x.dst)

  def __getitem__(self, dst: int) -> int:
    for rng in self.ranges:
      if rng.has(dst): return rng[dst]
    return dst

  def map_range(self, seeds: SeedRng) -> Iterable[SeedRng]:
    while seeds.len:
      for i, cr in enumerate(self.ranges):
        start = seeds.start
        supported = False
        if i == 0 and start < cr.dst:
          n_supported = min(seeds.len, self.ranges[0].dst)
          yield SeedRng(start, n_supported)
          seeds = SeedRng(start + n_supported, seeds.len - n_supported)
        elif cr.has(start):
          n_supported = cr.supports(seeds)
          yield SeedRng(cr[start], n_supported)
          seeds = SeedRng(start + n_supported, seeds.len - n_supported)
        elif not cr.has(start) and i < len(self.ranges) - 1 and start < self.ranges[i + 1].dst:
          n_supported = min(seeds.len, self.ranges[i + 1].dst - start)
          yield SeedRng(start, n_supported)
          seeds = SeedRng(start + n_supported, seeds.len - n_supported)
        elif i == len(self.ranges) - 1 and start > cr.dst:
          n_supported = seeds.len
          yield SeedRng(start, n_supported)
          seeds = SeedRng(start + n_supported, seeds.len - n_supported)

          

def parse(s: str) -> tuple[list[int], list[Compat]]:
    raw_seeds, *raw_maps = s.split('\n\n')
    seeds = [int(x) for x in raw_seeds.split(' ')[1:]]
    maps = []
    for raw_map in raw_maps:
      raw_ranges = raw_map.split('\n')[1:]
      maps.append([
        CompatRng(*(int(x) for x in raw_range.split(' ')))
        for raw_range in raw_ranges])
    return seeds, [Compat(mapping) for mapping in maps]
  
def part1(seeds: Iterable[int], maps: Iterable[Compat]) -> int:
  smallest = None
  for seed in seeds:
    x = seed
    for compat in maps: x = compat[x]
    if smallest is None or x < smallest: smallest = x
  if smallest is None: raise RuntimeError('Nothing found')
  return smallest
  
def part2(seeds: list[int], maps: list[Compat]) -> int:
  seed_ranges = [SeedRng(s1, s2) for s1, s2 in zip(seeds[::2], seeds[1::2])]
  for compat in maps:
    seed_ranges = list(itertools.chain(*(compat.map_range(sr) for sr in seed_ranges)))
  return min(seed_ranges, key=lambda sr: sr.start).start

def main():
  for filename in sys.argv[1:]:
    with open(filename) as f: data = f.read().strip('\n')
    seeds, maps = parse(data)
    print(part1(seeds, maps))
    print(part2(seeds, maps))

if __name__ == '__main__':
  main()
