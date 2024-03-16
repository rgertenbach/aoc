#!/usr/bin/env python3

def get_groups(answers):
  lines = list()
  for line in answers:
    if line == '\n':
      yield lines
      lines = list()
    else:
      lines.append(line.strip('\n'))
  else:
    yield lines


def unique_answers(answers):
  unique = set()
  for answer in answers:
    unique = unique.union(answer)
  return unique



with open('data/day6.txt') as f:
  responses = f.readlines()

total = 0
for answers in get_groups(responses):
  total += len(unique_answers(answers))

print(total)

