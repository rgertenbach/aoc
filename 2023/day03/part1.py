#! /home/robin/py/venv/bin/python4

import sys
import string
from typing import Iterator

def is_digit(c: str) -> bool: return c in string.digits
def is_empty(c: str) -> bool: return c == '.'
def is_symbol(c: str) -> bool: return not is_digit(c) and not is_empty(c)

def extract_digit(line: str, start: int) -> int:
  end = start + 1
  while end < len(line) and is_digit(line[end]): end += 1
  return int(line[start:end])

def is_part(schematic: list[str], row: int, col: int) -> bool:
  rows = len(schematic)
  line = schematic[row]
  if col:
    if is_symbol(line[col - 1]): return True
    if row and is_symbol(schematic[row - 1][col - 1]): return True
    if row < rows - 1 and is_symbol(schematic[row + 1][col - 1]): return True

  for off in range(col, len(line)):
    if row and is_symbol(schematic[row - 1][off]): return True
    if row < rows - 1 and is_symbol(schematic[row + 1][off]): return True
    if not is_digit(line[off]): return is_symbol(line[off])

  return False

def part_numbers(schematic: list[str]) -> Iterator[int]:
  in_number = False
  for row, line in enumerate(schematic):
    for col, c in enumerate(line):
      if not is_digit(c):
        in_number = False
        continue
      if in_number: continue
      if is_part(schematic, row, col):
        in_number = True
        yield extract_digit(line, col)

def main():
  for filename in sys.argv[1:]:
    with open(filename) as f: 
      schematic = f.read().strip('\n').split('\n')
      print(sum(part_numbers(schematic)))

if __name__ == '__main__':
  main()
