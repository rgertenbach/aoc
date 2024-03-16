with open('input.txt') as f:
  ops = f.read().strip().split('\n')

CYCLES = {
    'addx': 2,
    'noop': 1
}


CHECK_INT = 40
CHECK_OFF = 20

def is_checkpoint(cycle):
  return (cycle - CHECK_OFF) % CHECK_INT == 0

x = 1
total_strength = 0
elapsed = 1


for op in ops:
  amt = 0
  if op != 'noop':
    op, amt = op.split(' ')

  cycles = CYCLES[op]

  if is_checkpoint(elapsed):
    total_strength += elapsed * x
  elif op == 'addx' and is_checkpoint(elapsed + 1):
    total_strength += (elapsed + 1) * x

  x += int(amt)
  elapsed += CYCLES[op]

if is_checkpoint(elapsed):
    total_strength += elapsed * x
print(total_strength)
