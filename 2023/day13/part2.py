import sys


def reflection_line(pattern: list[str], exclude: int | None = None) -> int:
  rows = len(pattern)
  for i in range(1, rows):
    if exclude is not None and i == exclude: continue
    top = i - 1
    bottom = i

    while True:
      if pattern[top] != pattern[bottom]: break
      if top == 0 or bottom == rows - 1: break
      top -= 1
      bottom += 1
    if (top == 0 or bottom == rows - 1) and pattern[top] == pattern[bottom]:
      return i
  return 0


def points(orig: list[str]) -> int:
  rows = reflection_line(orig)
  cols = reflection_line(transpose(orig))
  if rows and cols: return 0
  return 100 * rows + cols

def p2(orig: list[str], old: list[str]) -> int:
  o_rows = reflection_line(old)
  o_cols = reflection_line(transpose(old))
  rows = reflection_line(orig, o_rows)
  cols = reflection_line(transpose(orig), o_cols)
  return (
      100 * (0 if rows == o_rows else rows)
      + (0 if cols == o_cols else cols))

def swap(ss: list[str], r: int, c: int) -> list[str]:
  out = []
  for row, line in enumerate(ss):
    newline = []
    for col, char in enumerate(line):
      if row == r and col == c: newline.append('.' if char == '#' else '#')
      else: newline.append(char)
    out.append(''.join(newline))
  return out


def points2(orig: list[str]) -> int:
  for row in range(len(orig)):
    for col in range(len(orig[0])):
      pts = p2(swap(orig, row, col), orig)
      if pts: return pts
  print('aaah')
  return 0

def part1(orig: list[list[str]]) -> int: return sum(points(o) for o in orig)
def part2(orig: list[list[str]]) -> int: return sum(points2(o) for o in orig)
def transpose(ss: list[str]) -> list[str]: return [''.join(x) for x in zip(*ss)]


def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: data = f.read().strip()
    raw_patterns: list[str] = data.split('\n\n')
    orig = [pattern.split('\n') for pattern in raw_patterns]

    print('Part 1:', part1(orig))
    print('Part 2:', part2(orig))

# part 1needs to be 37381
# part 2 needs to be less than 36982 and more than 19820

if __name__ == '__main__':
  main()
