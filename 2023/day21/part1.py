import sys


START = 'S'
PLOT = '.'
ROCK = '#'


def part1(garden: list[list[str]]) -> int:
  start_row = -1
  start_col = -1
  for row, line in enumerate(garden):
    for col, c in enumerate(line):
      if c == START:
        start_row = row
        start_col = col
        break;
  if start_row + start_col < 0: raise RuntimeError()

  pos = [(start_row, start_col)]
  for i in range(64):
    new_pos = set()
    for row, col in pos:
      if row and garden[row - 1][col] != ROCK: new_pos.add((row - 1, col))
      if row < len(garden) - 1 and garden[row + 1][col] != ROCK: new_pos.add((row + 1, col))
      if col and garden[row][col - 1] != ROCK: new_pos.add((row, col - 1))
      if col < len(garden[0]) - 1 and garden[row][col + 1] != ROCK: new_pos.add((row, col + 1))
    pos = list(new_pos)
  return len(pos)





def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: data = f.read().strip()
    garden = [list(row) for row in data.split('\n')]
    print(part1(garden))


if __name__ == '__main__':
  main()
