import sys

ASH = '.'
ROCK = '#'

Pattern = list[str]

newline = '\n'

def reflection_line(pattern) -> int:
  rows = len(pattern)
  has_match = False
  for i in range(1, rows):
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


def p1points(orig, rotated) -> int:
  rows = reflection_line(orig)
  cols = reflection_line(rotated)
  return 100 * rows + cols


def part1(orig, rotated) -> int:
  return sum(p1points(o, r) for o, r in zip(orig, rotated))


def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f:
      orig = [pattern.split('\n') for pattern in f.read().strip().split('\n\n')]
    rotated = [[''.join(x) for x in zip(*o)] for o in orig]

    print('Part 1:', part1(orig, rotated))

# input needs to be greater than 31318

if __name__ == '__main__':
  main()
