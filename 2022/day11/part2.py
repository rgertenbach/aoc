from collections import deque

with open('input.txt') as f:
  monkeys = f.read().split('\n\n')

class Op:
  def __init__(self, s: str):
    parts = s.split(' ')
    self.left = parts[0] if parts[0] == 'old' else int(parts[0])
    self.right = parts[2] if parts[2] == 'old' else int(parts[2])
    self.op = parts[1]

  def apply(self, worry: int) -> int:
    fun = {
        '+': lambda a, b: a + b,
        '*': lambda a, b: int(a * b)}[self.op]
    left = worry if self.left == 'old' else self.left
    right = worry if self.right == 'old' else self.right
    return fun(left, right)

  def __str__(self) -> str:
    return f'{self.left}{self.op}{self.right}'


class Monkey:
  def __init__(self, s):
    lines = s.split('\n')[1:]  # Skip Monkey id.
    self.items = deque(
        int(worry) 
        for worry 
        in lines[0].strip().replace('Starting items: ', '').split(', '))
    self.op = Op(lines[1].strip().replace('Operation: new = ', ''))
    self.mod_test = int(lines[2].strip().replace('Test: divisible by ', ''))
    self.mod_then = int(lines[3][-1])
    self.mod_else = int(lines[4][-1])
    self.n_inspected = 0

  def __str__(self):
    return (
        f'Has {self.items}, does {self.op}. If divisible by {self.mod_test} '
        f'then {self.mod_then} else {self.mod_else} and inspected '
        f'{self.n_inspected} items')

  def catch(self, worry: int) -> None:
    self.items.append(worry)

  @property
  def has_items(self) -> bool:
    return len(self.items) > 0

  def target_monkey(self, worry: int) -> int:
    return self.mod_then if worry % self.mod_test == 0 else self.mod_else    

  def inspect(self, monkeys: list['Monkey']) -> None:
    while self.has_items:
      self.n_inspected += 1
      item = self.items.popleft()
      item = self.op.apply(item)
      target = self.target_monkey(item)
      monkeys[target].catch(item)

  def normalize(self, factor: int) -> None:
    normalized = []
    while self.has_items:
      normalized.append(self.items.popleft() % factor)

    self.items = deque(normalized)


def one_round(monkeys: list[Monkey], factor: int) -> None:
  for monkey in monkeys:
    monkey.inspect(monkeys)
  for monkey in monkeys:
    monkey.normalize(factor)


monkeys = [Monkey(monkey) for monkey in monkeys]
normalization_factor = 1
for monkey in monkeys:
  normalization_factor *= monkey.mod_test


for i in range(10000):
  if i % 100 == 0:
    print(f'Round {i}')
  one_round(monkeys, normalization_factor)

inspections = sorted([monkey.n_inspected for monkey in monkeys])


print(inspections[-1] * inspections[-2])

