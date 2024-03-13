import sys

def hash(s: str) -> int:
  value = 0
  for c in s:
    value += ord(c)
    value *= 17
    value %= 256
  return value

def part1(s: str) -> int:
  return sum(hash(x) for x in s.split(','))

def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: data = f.read().strip()
    print(part1(data))


if __name__ == '__main__':
  main()
