#!/usr/bin/env python3
import re
from collections import defaultdict
from functools import cache


def parse_content(content):
  m = re.match(r'(no|\d+) (.+)$', content)
  n, bag = m.groups()
  if n == 'no':
    n = 0
  if not bag.endswith('s'):
    bag = bag + 's'
  return bag, n


def parse_rule(rule):
  key, contents = rule.split(' contain ')
  contents = contents.strip('\n.').split(', ')
  contents = [parse_content(content) for content in contents]
  return key, contents


@cache
def count_children(parent):
  children = rules[parent]
  n = 0
  for child, n_children in children:
    if child == 'other bags':
      continue
    n += int(n_children)
    n += int(n_children) * count_children(child)  
  return n


with open('data/day7.txt') as f:
  rules = f.readlines()

rules = [parse_rule(rule) for rule in rules]
rules = dict(rules)
print(count_children('shiny gold bags'))

