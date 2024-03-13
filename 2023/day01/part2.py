import re
import sys

DIGITS = {
    'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
    'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
}

def load_data(filename: str):
  with open(filename) as f:
    return [*f.readlines()]

def parse_line(line: str) -> int:
  pat = '(' + '|'.join([*DIGITS.keys()] + [str(x) for x in range(10)]) + ')'
  left = re.search('^.*?' + pat, line)
  if left is None: raise RuntimeError('fo')
  left = left[1]
  left = DIGITS.get(left, left)
  right = re.search('.*' + pat + '.*?$', line)
  if right is None: raise RuntimeError('bar')
  right = right[1]
  right = DIGITS.get(right, right)
  return int(left + right)

def main():
  lines = load_data(sys.argv[1])
  digits = [parse_line(line) for line in lines]
  print(sum(digits))

if __name__ == '__main__':
  main()
