#!/usr/bin/python3
import sys

# wrong close -> corrput
# incomplete -> missing close

# Get corrupt
# Get incorrect closing character

VALUES = {
  ')': 1,
  ']': 2,
  '}': 3,
  '>': 4}

MATCH = {
  '(': ')',
  '[': ']',
  '{': '}',
  '<': '>'}

def wrong_close(line):
  "Returns the first illegal close, the unbalanced closing parens or None"
  stack = []
  opens, closes = zip(*MATCH.items())
  for c in line:
    if c in opens:
      stack.append(MATCH[c])
    else:  # Close
      if stack and c == stack[-1]:
        stack.pop()
      else:
        return c  # Corrupt closing Character
  if stack:
    return stack[-1::-1]
  return None

def points(cl):
  score = 0
  for close in cl:
    score *= 5
    score += VALUES[close]
  return score



def read_file(filename):
  with open(filename) as f:
    return [line.strip() for line in f.readlines()]

def main(filename):
  lines = read_file(filename)
  wrong_closes = [wrong_close(line) for line in lines]
  incomplete = [close for close in wrong_closes if type(close) == list]
  ps = [points(inc) for inc in incomplete]
  print(sorted(ps)[len(ps) // 2])

if __name__ == '__main__':
  main(*sys.argv[1:])


