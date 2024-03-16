with open('input.txt') as f:
  ops = f.read().strip().split('\n')

CYCLES = {
    'addx': 2,
    'noop': 1
}

WIDTH = 40
HEIGHT = 6
SPRITE_WIDTH = 3

def sprite_on(x: int, col: int) -> bool:
  return (x - 1) <= col <= (x + 1)

def light(cycle: int, x: int) -> None:
  col = cycle % WIDTH
  row = cycle // WIDTH
  if sprite_on(x, col):
    print(f'{row=}, {col=}, {x=}')
    crt[row][col] = '#'


x = 1
elapsed = 0
crt = [list('.' * WIDTH) for _ in range(HEIGHT)]

for op in ops:
  amt = 0
  if op != 'noop':
    op, amt = op.split(' ')

  for cycle in range(CYCLES[op]):
    light(elapsed, x)
    elapsed += 1
    if cycle == 1:
      x += int(amt)


print('\n'.join(''.join(row) for row in crt))


