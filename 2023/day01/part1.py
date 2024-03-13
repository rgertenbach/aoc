import re
import sys

def load_data(filename: str):
  with open(filename) as f:
    return [*f.readlines()]

def parse_line(line: str) -> int:
  pat = re.compile('[a-zA-Z]')
  digits = re.sub('[a-zA-Z]', '', line)
  return int(digits[0] + digits[-2])

def main():
  lines = load_data(sys.argv[1])
  digits = [parse_line(line) for line in lines]
  print(sum(digits))

if __name__ == '__main__':
  main()
