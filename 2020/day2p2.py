#!/usr/bin/env python3
import re

def is_valid(pw):
  p1, p2, letter, pw = re.match(r'^(\d+)-(\d+) ([\w]): (.+)', pw).groups()
  return (pw[int(p1)-1] == letter) ^ (pw[int(p2)-1] == letter)

with open('data/day2.txt') as f: passwords = f.readlines()
print(sum([is_valid(pw) for pw in passwords]))


