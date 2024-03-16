#!/usr/bin/python3
# Should give 5 / 5092

import sys

def parse_segment(seg):
  xs = seg.split(',')
  return tuple(int(x) for x in xs)


def parse_vent(vent):
  segs = vent.strip().split(' -> ')
  segs = tuple(parse_segment(seg) for seg in segs)
  return segs


def load_data(filename):
  vents = []
  with open(filename) as f:
    for line in f:
      vents.append(parse_vent(line))
  return vents


def is_straight(vent):
  x1, x2 = vent
  return x1[0] == x2[0] or x1[1] == x2[1]


def generate_points(v):
  (x1, y1), (x2, y2) = v
  x1, x2 = sorted([x1, x2])
  y1, y2 = sorted([y1, y2])
  return [(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)]

def overlapping_points(ps1, ps2):
  return [p1 for p1 in ps1 if p1 in ps2]

def straight_overlaps(vents):
  overlaps = []
  points = [generate_points(vent) for vent in vents]
  for vent1i, v1 in enumerate(points[:-1]):
    for v2 in points[(vent1i + 1):]:
      overlaps.extend(overlapping_points(v1, v2))
  return set(overlaps)
      

if __name__ == '__main__':
  vents = load_data(sys.argv[1])
  straight_vents = [vent for vent in vents if is_straight(vent)]
  overlaps = straight_overlaps(straight_vents)
  print(overlaps)
  print(len(overlaps))



