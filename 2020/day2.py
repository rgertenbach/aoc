#!/usr/bin/env python3
import re
from collections import Counter

def is_valid(pw):
  lower, upper, letter, pw = re.match(r'^(\d+)-(\d+) ([\w]): (.+)', pw).groups()
  freqs = Counter(pw)
  return int(lower) <= freqs[letter] <= int(upper)

with open('data/day2.txt') as f: passwords = f.readlines()
print(sum([is_valid(pw) for pw in passwords]))


