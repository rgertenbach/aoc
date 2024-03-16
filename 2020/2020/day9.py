#!/usr/bin/env python3

with open('data/day9.txt') as f:
  data = f.readlines()
data = [int(row.strip('\n')) for row in data]


def summable(number, components):
  for c1 in components:
    if number - c1 in components:
      return True
  return False


def find_violations(data, preamble):
  for i in range(preamble, len(data)):
    evalrange = data[i - preamble:i]
    evalcan = data[i]
    if not summable(evalcan, evalrange):
      return evalcan


def sumrange(value, data):
  for start in range(len(data)):
    total = data[start]
    for end in range(start + 1, len(data)):
      total += data[end]
      if total == value:
        return data[start:end + 1]
      elif total > value:
        break



vio = find_violations(data, 25)
print(vio)
target_range = sumrange(vio, data)
print(target_range)
print(min(target_range) + max(target_range))

