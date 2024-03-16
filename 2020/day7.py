#!/usr/bin/env python3
import re
from collections import defaultdict

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



with open('data/day7.txt') as f:
  rules = f.readlines()

rules = [parse_rule(rule) for rule in rules]
rules = dict(rules)

inverse = defaultdict(list)
for container, contents in rules.items():
  for content in contents:
    inverse[content[0]].append(container)

def count_parents(leaf, start = set()):
  parents = set(inverse[leaf])
  grandparents = [count_parents(parent) for parent in parents]
  for grandparentset in grandparents:
    parents = parents.union(grandparentset)
  return parents
  

want = 'shiny gold bags'
print(len(count_parents(want)))



