from collections import deque
import sys

ROUND = 'O'
CUBE = '#'
EMPTY = '.'

def transpose(ss: list[list[str]]) -> list[list[str]]:
  return [[*x] for x in zip(*ss)]

def count_series(ss: list[str]) -> deque[tuple[str, int]]:
  counts = deque()
  last = ss[0]
  n = 1
  for x in ss[1:]:
    if x == last: n += 1
    else:
      counts.append((last, n))
      n = 1
      last = x
  counts.append((last, n))
  return counts


def roll(s: list[str]) -> list[str]:
  counts = count_series(s)
  out = []
  while counts:
    x, freq = counts.popleft()
    if x == EMPTY and counts and counts[0][0] == ROUND:
      _, n_round = counts.popleft()
      out.extend(ROUND * n_round)
      if counts and counts[0][0] == EMPTY:
        _, next_empty_freq = counts.popleft()
        counts.appendleft((EMPTY, freq + next_empty_freq))
      else: counts.appendleft((EMPTY, freq))
    else:
      out.extend(x * freq)
  return out


def up(lines: list[list[str]]) -> list[list[str]]:
  return transpose([roll(col) for col in transpose(lines)])

def load(lines: list[list[str]]) -> int:
  n = len(lines)
  total = 0
  for i, line in enumerate(lines):
    total += (n - i) * sum(x == ROUND for x in line)
  return total



def part1(lines: list[list[str]]) -> int:
  upped = up(lines)
  return load(upped)

def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f:
      lines = [list(x) for x in f.read().strip().split('\n')]
    print(part1(lines))

if __name__ == '__main__':
  main()
