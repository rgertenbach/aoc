import sys
from typing import NamedTuple
import re

REMOVE = '-'
INSERT = '='


def hash256(s: str) -> int:
  value = 0
  for c in s:
    value += ord(c)
    value *= 17
    value %= 256
  return value

class Operation(NamedTuple):
  label: str
  box: int
  op: str
  focal: int = 0

  @classmethod
  def parse(cls, s: str) -> 'Operation':
    result = re.match(r'([^=-]+)([=-])(\d*)', s)
    if result is None: raise RuntimeError(f'No match for {s}')
    match list(result.groups()):
      case [str() as label, '-', '']:
        return cls(label, hash256(label), REMOVE)
      case [str() as label, '=', str() as f]:
        return cls(label, hash256(label), INSERT, int(f))
    raise RuntimeError(f'Unparseable {s}')


class Initialization:
  def __init__(self):
    self.boxes = [[] for _ in range(256)]
    self.lenses = {}

  def do(self, op: Operation) -> None:
    if op.op == REMOVE: self.remove(op.label, op.box)
    else: self.insert(op.label, op.box, op.focal)
    # print('After', op, '\n', self)

  def remove(self, label: str, box: int) -> None:
    if label in self.lenses:
      self.boxes[box] = [lens for lens in self.boxes[box] if lens != label]
      del self.lenses[label]

  def insert(self, label: str, box: int, focal: int) -> None:
    if label in self.lenses: self.lenses[label] = focal
    else:
      self.lenses[label] = focal
      self.boxes[box].append(label)

  def __str__(self) -> str:
    boxes = [
        f'Box {boxi}: ' + ' '.join(f'[{lens} {self.lenses[lens]}]' for lens in box)
        for boxi, box in enumerate(self.boxes)
        if box
    ]
    newline = '\n'
    return f'''Initialization:
{newline.join(boxes)}
    '''

  def focusing_power(self) -> int:
    total = 0
    for boxi, box in enumerate(self.boxes):
      for lensi, lens in enumerate(box):
        total += (boxi + 1) * (lensi + 1) * self.lenses[lens]
    return total



# keep track of where each lens is

def part1(ops: list[str]) -> int: return sum(hash256(x) for x in ops)

def part2(ops_raw: list[str]) -> int:
  ops = [Operation.parse(op) for op in ops_raw]
  init = Initialization()
  for op in ops:
    init.do(op)
  return init.focusing_power()

def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: data = f.read().strip()
    ops = data.split(',')
    print(part1(ops))
    print(part2(ops))


if __name__ == '__main__':
  main()
