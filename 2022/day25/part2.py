DECODE = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}


ENCODE = {
    -2: '=',
    -1: '-',
    0: '0',
    1: '1',
    2: '2',
}


def parse_snafu(snafu: str) -> int:
  stack = list(snafu)
  po5 = 1
  out = 0
  while stack:
    out += po5 * DECODE[stack.pop()]
    po5 *= 5
  return out

  
def make_snafu(v: int) -> str:
  stack = []

  rem = 0
  while v:
    x = v % 5 + rem
    v //= 5
    rem = 0
    
    if x >= 3:
      x = x - 5
      rem = 1
    stack.append(ENCODE[x])
  if rem:
    stack.append('1')



  return ''.join(reversed(stack))


def fuel_needed(filepath: str) -> str:
  with open(filepath) as f:
    snafus = f.read().strip().split('\n')
  total = sum(parse_snafu(snafu) for snafu in snafus)
  return make_snafu(total)


print(fuel_needed('input.txt'))
