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

def down(lines: list[list[str]]) -> list[list[str]]:
  return transpose([roll(col[::-1])[::-1] for col in transpose(lines)])

def left(lines: list[list[str]]) -> list[list[str]]:
  return [roll(col) for col in lines]

def right(lines: list[list[str]]) -> list[list[str]]:
  return [roll(col[::-1])[::-1] for col in lines]

def cycle(lines: list[list[str]]) -> list[list[str]]:
  return right(down(left(up(lines))))

def load(lines: list[list[str]]) -> int:
  n = len(lines)
  total = 0
  for i, line in enumerate(lines):
    total += (n - i) * sum(x == ROUND for x in line)
  return total

def part1(lines: list[list[str]]) -> int:
  upped = up(lines)
  return load(upped)

def is_cycle(s: list[int], start: int, cycle_len: int) -> bool:
  for i in range(cycle_len):
    x = s[start + i]
    off = 1
    while (next_i := start + off * cycle_len + i) < len(s):
      if x != s[next_i]: return False
      off += 1
  return True


def detect_cycle(s: list[int]) -> tuple[int, int]:
  for start in range(len(s)):
    for cycle_len in range(1, len(s) // 2):
      if is_cycle(s, start, cycle_len): return start, cycle_len
  return -1, -1


def part2(lines: list[list[str]]) -> int:
  "109325 is too high"

  nth = 1_000_000_000
  loads = []
  for _ in range(1000): 
    lines = cycle(lines)
    loads.append(load(lines))
  cycle_offset, cycle_len = detect_cycle(loads)
  loads = loads[cycle_offset:]
  loads = loads[:cycle_len]
  nth -= cycle_offset
  return loads[nth % cycle_len - 1]



def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f:
      lines = [list(x) for x in f.read().strip().split('\n')]
    print(f'part 1: {part1(lines)}')
    print(f'part 2: {part2(lines)}')

if __name__ == '__main__': main()
