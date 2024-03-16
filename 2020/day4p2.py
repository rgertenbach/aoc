#!/usr/bin/env python3
import re


with open('data/day4.txt') as f:
  passports = f.readlines()

def get_passports(passports):
  passport = {}
  for row in passports:
    if row == '\n':
      yield passport
      passport = {}
    else:
      row = row.strip('\n')
      pairs = row.split(' ')
      for pair in pairs:
        k, v = pair.split(':')
        passport[k] = v
  else:
    yield passport


def validate_passport(pp):
  valid = True
  wanted = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
  if not set(pp.keys()).issuperset(wanted):
    return False

  for k, v in pp.items():
    if k == 'byr':
      if re.match(r'(\d{4})$', v) is None or not (1920 <= int(v) <= 2002):
        return False
    elif k == 'iyr':
      if re.match(r'(\d{4})$', v) is None or not (2010 <= int(v) <= 2020):
        return False
    elif k == 'eyr':
      if re.match(r'(\d{4})$', v) is None or not (2020 <= int(v) <= 2030):
        return False
    elif k == 'hgt':
      match = re.match(r'(\d+)(in|cm)$', v)
      if match is None:
        return False
      height, unit = match.groups()
      if unit == 'cm':
        if not 150 <= int(height) <= 193:
          return False
      elif unit == 'in':
        if not 59 <= int(height) <= 76:
          return False
      else: 
        return False
    elif k == 'hcl':
      if re.match('#[0-9a-f]{6}$', v) is None:
        return False
    elif k == 'ecl':
      if v not in ('amb,blu,brn,grn,gry,hzl,oth'.split(',')):
        return False
    elif k == 'pid':
      if re.match(r'\d{9}$', v) is None:
        return False
  return True



valid = 0
got = set()
kvs = {}
for passport in get_passports(passports):
  valid += validate_passport(passport)


print(valid)
  



