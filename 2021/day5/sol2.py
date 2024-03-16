#!/usr/bin/python3
# Should give 5 / 5092
# We only care about straights and diagonals!

import sys
from point import Point
from segment import Direction, Segment


def load_data(filename):
  vents = []
  with open(filename) as f:
    for line in f:
      vents.append(Segment.parse(line))
  return vents


if __name__ == '__main__':
  vents = load_data(sys.argv[1])
  straight_vents = [vent 
                    for vent in vents 
                    if vent.direction != Direction.DIAGONAL]
  overlaps = []
  for i, vent1 in enumerate(straight_vents[:-1]):
    for vent2 in straight_vents[i+1:]:
      overlaps.extend(vent1.overlaps(vent2) or [])

  overlaps = set(overlaps)
  print(len(overlaps))


  



