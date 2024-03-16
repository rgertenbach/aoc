#!/usr/bin/python3
import sys
from beacon import Beacon
from scanner import Scanner

# I currentlt have 4^3 = 48 rotations, no 24
# two scanners must share at least 12 beacons
# need to get unique # of beacons


def read_file(filename):
  with open(filename) as f:
    lines = f.read()
  scanners = lines.split('\n\n')
  return [Scanner.parse(scanner, i) for i, scanner in enumerate(scanners)]

def find_overlaps(s1, s2):
  "Currently counts the # of rotations that lead to 12+ overlaps"
  perms = s2.permutations()
  outcomes = 0
  for i, perm in enumerate(perms):
    overlaps = s1.overlaps(perm)
    if overlaps:
      outcomes += 1
  return outcomes

def identify_overlaps(s1, s2):
  "Assumes exactly one possible rotation with 12+ overlaps"
  perms = s2.permutations()
  for perm in perms:
    overlaps = s1.overlaps(perm)
    if overlaps:
      return perm, overlaps

def maybe_merge(s1, s2):
  "Shouldnt be used, it's always pairs of scanners"
  perms = s2.permutations()
  for perm in perms:
    out = s1.merge(perm)
    if out is not None:
      return out
  return None

def align_scanners(scanners):
  out, remaining = [[scanners[0]], scanners[1:]]
  while remaining:
    for o in out:
      for i, s in enumerate(remaining):
        print(f'Comparing {o.scanner_id} vs {s.scanner_id}')
        res = identify_overlaps(o, s)
        if res is not None:
          print(f'Added scaner {s.scanner_id}.')
          out.append(res[0])
          remaining = [r for j, r in enumerate(remaining) if j != i]
          break
  return out




scanners = read_file(sys.argv[1])
n_scanners = len(scanners)


res, remaining = scanners[0], scanners[1:]
while remaining:
  for i, rem in enumerate(remaining):
    print('Checking', rem.scanner_id)
    tres = maybe_merge(res, rem)
    print('Done Checking')
    if tres is not None:
      res = tres
      remaining = [r for i2, r in enumerate(remaining) if i2 != i]
      print('Added scanner', rem.scanner_id)
      break;


