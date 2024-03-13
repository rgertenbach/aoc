import sys
import string
from typing import Iterator

def is_digit(c: str) -> bool: return c in string.digits

def extract_digit(line: str, start: int) -> tuple[int, int]:
  end = start + 1
  while end < len(line) and is_digit(line[end]): end += 1
  return int(line[start:end]), end - 1

def find_digit_start(line: str, start: int) -> int:
  while start:
    if is_digit(line[start - 1]): start -= 1
    else: break
  return start

def identify_numbers(schematic: list[str], row: int, col: int) -> list[int]:
  line = schematic[row]
  rows = len(schematic)
  out = []
  end = -100
  # checking above and below
  other_lines = []
  if row > 0: other_lines.append(schematic[row - 1])
  if row < rows - 1: other_lines.append(schematic[row + 1])
  for pline in other_lines:
    if row > 0:
      if col > 0:
        if is_digit(pline[col - 1]):
          start = find_digit_start(pline, col - 1)
          number, end = extract_digit(pline, start)
          out.append(number)
      if end < col - 1:
        if is_digit(pline[col]):
          start = find_digit_start(pline, col)
          number, end = extract_digit(pline, start)
          out.append(number)
      if end < col and col < len(line) - 1:
        if is_digit(pline[col + 1]):
          start = find_digit_start(pline, col + 1)
          number, end = extract_digit(pline, start)
          out.append(number)
    end = -100
  # left
  if col > 0:
    if is_digit(line[col - 1]):
      start = find_digit_start(line, col - 1)
      number, end = extract_digit(line, start)
      out.append(number)
  if end < col and col < len(line) - 1:
    if is_digit(line[col + 1]):
      start = find_digit_start(line, col + 1)
      number, end = extract_digit(line, start)
      out.append(number)

  return out

  

def find_gears(schematic: list[str]) -> Iterator[int]:
  for row, line in enumerate(schematic):
    for col, c in enumerate(line):
      if c != '*': continue
      numbers = identify_numbers(schematic, row, col)
      if len(numbers) != 2: continue
      print(f'{numbers[0]} * {numbers[1]} = {numbers[0] * numbers[1]}')
      yield numbers[0] * numbers[1]

def main():
  for filename in sys.argv[1:]:
    with open(filename) as f:
      schematic = f.read().strip('\n').split('\n')
    print(sum(find_gears(schematic)))

if __name__ == '__main__':
  main()
