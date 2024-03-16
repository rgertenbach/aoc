#!/usr/bin/env python3

wanted = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])

with open('data/day4.txt') as f:
  passports = f.readlines()

valid = 0
got = set()
for row in passports:
  if row == '\n':
    if got.issuperset(wanted):
      valid += 1
    got.clear()
    continue
  pairs = row.split(" ")
  kvs = [kv.split(":") for kv in pairs]
  keys = set(kv[0] for kv in kvs)
  got = got.union(keys)
else: 
  if row != '\n':
    if got.issuperset(wanted):
      valid += 1


print(valid)
  



