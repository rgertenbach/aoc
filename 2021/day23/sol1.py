#!/usr/bin/env python3

import sys

from pod import Pod, Cave

# def read_file(filename):
#   with open(filename) as f:
#     return Cave.parse(f.readlines())

# print(read_file(sys.argv[1]))

pods = [
  Pod('b', 11), Pod('a', 12),
  Pod('c', 13), Pod('d', 14),
  Pod('b', 15), Pod('c', 16),
  Pod('d', 17), Pod('a', 18)]

cave = Cave(pods)

print(str(cave))

for pod in cave.to_move:
  print(pod)
