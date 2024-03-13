import sys
import itertools

OPERATIONAL = '.'
DAMAGED = '#'
UNKNOWN = '?'

class Record:
  def __init__(self, springs: list[str], damaged: list[int]):
    self.springs = springs
    self.damaged = damaged
    self.total_damaged = sum(self.damaged)
    self.current_damaged = sum(x == DAMAGED for x in self.springs)
    self.current_unknown = sum(x == UNKNOWN for x in self.springs)

  @classmethod
  def parse(cls, s: str) -> 'Record':
    springs, damaged_raw = s.split(' ')
    return cls(list(springs), [int(x) for x in damaged_raw.split(',')])

  def __str__(self) -> str:
    return f'{"".join(self.springs):<30}{",".join(str(x) for x in self.damaged)}'
  
  def __len__(self) -> int: return len(self.springs)

  def ways_to_complete(self) -> int:
    total = 0
    unknown_indices = [i for i, s in enumerate(self.springs) if s == UNKNOWN]
    to_allocate = self.total_damaged - self.current_damaged
    
    for combination in itertools.combinations(unknown_indices, to_allocate):
      if self.recreate(combination).is_legal(): total += 1

    return total

  def recreate(self, damaged: list[int]) -> 'Record':
    new_springs = [x for x in self.springs]
    for i in damaged: new_springs[i] = DAMAGED
    for i, spring in enumerate(new_springs):
      if spring == UNKNOWN: new_springs[i] = OPERATIONAL
    return Record(new_springs, self.damaged)

  def is_legal(self) -> bool:
    dmgi = 0
    dmg = 0
    for i, spring in enumerate(self.springs):
      if spring == DAMAGED:
        dmg += 1
        if dmgi >= len(self.damaged): return False
        if self.damaged[dmgi] < dmg: return False
      elif i and self.springs[i - 1] == DAMAGED:
        dmg = 0
        dmgi += 1
    return True


def parse(s: str) -> list[Record]: return [Record.parse(line) for line in s.split('\n')]

def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f:
      data = f.read().strip()
    report = parse(data)
    print('Part 1:', sum(record.ways_to_complete() for record in report))

if __name__ == '__main__':
  main()
