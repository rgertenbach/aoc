#!~/py/venv/bin/python3

from collections import namedtuple
import re

Point = namedtuple('Point', ['x', 'y'])
Line = namedtuple('Point', ['start', 'end'])

def parse_line(line: str) -> Line:
  match = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line)
  if match is None:
    raise RuntimeError(f'Could not parse line "{line}"')
  return Line(Point(match[1], match[2]), Point(match[3], match[4]))


def load_lines(filepath: str) -> list[Line]:
  lines = []
  with open(filepath) as f:
    for line in f:
      lines.append(parse_line(line))
  return lines


def is_diagonal(line: Line) -> bool:
  return line.start.x != line.end.x and line.start.y != line.end.y


def intersect(l1: Line, l2: Line) -> bool:
  x_overlap = l1.start.x <= l2.start.x <= l1.end.x or l1.start.x <= l2.end.x <= l1.end.x
  y_overlap = l1.start.y <= l2.start.y <= l1.end.y or l1.start.y <= l2.end.y <= l1.end.y
  return x_overlap or y_overlap



def main():
  lines = load_lines('test_input.txt')
  lines = [line for line in lines if not is_diagonal(line)]
  print(lines)
  # overlaps = 0
  # for i, l1 in enumerate(lines):
  #   for l2 in lines[i + 1:]:
  #     overlaps += intersect(l1, l2) + overlap(l1, l2)

  # print(overlaps)


if __name__ == '__main__':
  main()
