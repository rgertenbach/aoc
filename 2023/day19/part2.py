import re
import sys
from typing import NamedTuple
from enum import Enum

OPEN = '{'
CLOSE = '}'

ACCEPT = 'A'
REJECT = 'R'
NONE = ''

class Comparison(Enum):
  LESS_THAN = '<'
  GREATER_THAN = '>'
  NONE = ''

Part = dict[str, int]

class RatingRange(NamedTuple):
  min: int
  max: int

  @classmethod
  def base_case(cls) -> 'RatingRange':
    return cls(1, 4_000)

  def __str__(self) -> str:
    return f'{self.min}->{self.max}'

  def __repr__(self) -> str:
    return str(self)

  @property
  def size(self):
    return 1 + (self.max - self.min)

  def update(self, lower: int | None = None, upper: int | None = None) -> 'RatingRange':
    return self.__class__(
        self.min if lower is None else lower,
        self.max if upper is None else upper)

  def split(self, threshold: int, comparison: Comparison) -> tuple['RatingRange | None', 'RatingRange | None']:
    if comparison is Comparison.LESS_THAN:
      if threshold < self.min: return None, self
      if threshold > self.max: return self, None
      return self.update(upper=threshold - 1), self.update(lower=threshold)
    if comparison is Comparison.GREATER_THAN:
      if threshold < self.min: return self, None
      if threshold > self.max: return None, self
      return self.update(lower=threshold + 1), self.update(upper=threshold)
    raise RuntimeError('This should not happen')


class RangePart(NamedTuple):
  x: RatingRange
  s: RatingRange
  a: RatingRange
  m: RatingRange

  def get(self, key: str) -> RatingRange:
    if key == 'x': return self.x
    if key == 's': return self.s
    if key == 'a': return self.a
    if key == 'm': return self.m
    raise RuntimeError(f'key {key} not supported')

  def split_at(self, field: str, threshold: int, comparison: Comparison) -> tuple['RangePart | None', 'RangePart | None']:
    x, s, a, m = self
    if field == 'x':
      c0, c1 = x.split(threshold, comparison)
      return (
          None if c0 is None else self.__class__(c0, s, a, m), 
          None if c1 is None else self.__class__(c1, s, a, m))
    if field == 's':
      c0, c1 = s.split(threshold, comparison)
      return (
          None if c0 is None else self.__class__(x, c0, a, m), 
          None if c1 is None else self.__class__(x, c1, a, m))
    if field == 'a':
      c0, c1 = a.split(threshold, comparison)
      return (
          None if c0 is None else self.__class__(x, s, c0, m), 
          None if c1 is None else self.__class__(x, s, c1, m))
    c0, c1 = m.split(threshold, comparison)
    return (
        None if c0 is None else self.__class__(x, s, a, c0), 
        None if c1 is None else self.__class__(x, s, a, c1))
      
  @property
  def size(self) -> int:
    return self.x.size * self.s.size * self.a.size * self.m.size


def parse_part(s: str) -> dict[str, int]:
  out = {}
  components = s.strip('{}').split(',')
  for component in components:
    name, amt = component.split('=')
    out[name] = int(amt)
  return out

class Rule(NamedTuple):
  action: str
  field: str = NONE
  comp: Comparison = Comparison.NONE
  threshold: int = 0

  def __str__(self) -> str:
    return f'Rule({self.field}{self.comp.value}{self.threshold}: {self.action})'
  def __repr__(self) -> str:
    return str(self)

  @classmethod
  def parse(cls, s: str) -> 'Rule':
    if ':' not in s: return cls(s)
    comp, action = s.split(':')
    mat = re.match(r'([amsx])([<>])(\d+)', s)
    if mat is None: raise RuntimeError(f'Could not parse {s}')
    field, comp, thresh = mat.groups()
    return cls(action, field, Comparison(comp), int(thresh))

  def evaluate(self, part: Part) -> str:
    if self.comp is Comparison.NONE: return self.action
    if self.comp is Comparison.LESS_THAN and part[self.field] < self.threshold: return self.action
    if self.comp is Comparison.GREATER_THAN and part[self.field] > self.threshold: return self.action
    return NONE

  def evaluate_range(self, part: RangePart) -> tuple[
      int, 
      tuple[str, RangePart] | None,
      RangePart | None]:
    "Returns # of accepted parts, the range passing the threshold and the range not passing the threshold"
    if self.comp is Comparison.NONE:
      if self.action == ACCEPT: return part.size, None, None
      if self.action == REJECT: return 0, None, None
      return 0, (self.action, part), None
    success, failure = part.split_at(self.field, self.threshold, self.comp)
    if success is None: return 0, None, failure
    if self.action == ACCEPT: return success.size, None, failure
    if self.action == REJECT: return 0, None, failure
    return 0, (self.action, success), failure


class Workflow:
  def __init__(self, name: str, rules: list[Rule]):
    self.name = name
    self.rules = rules

  @classmethod
  def parse(cls, s: str) -> 'Workflow':
    name, rules_s = s.strip(CLOSE).split(OPEN)
    return cls(name, [Rule.parse(rule) for rule in rules_s.split(',')])

  def __str__(self) -> str: return f'{self.name}: {self.rules}'
  def __repr__(self) -> str: return str(self)

  def evaluate(self, part: Part) -> str:
    for rule in self.rules:
      result = rule.evaluate(part)
      if result != NONE: return result
    raise RuntimeError(f'{self} applied on {part} did not yield any result')

  def evaluate_range(self, part: RangePart) -> tuple[int, list[tuple[str, RangePart]]]:
    accepted = 0
    new_parts = []
    for rule in self.rules:
      a, r1, r2 = rule.evaluate_range(part)
      accepted += a
      if r1 is not None:
        new_parts.append(r1)
      if r2 is None: break
      part = r2
    return accepted, new_parts
    

def parse_input(s: str) -> tuple[dict[str, Workflow], list[Part]]:
  workflows_raw, parts_raw = s.split('\n\n')
  workflows = [Workflow.parse(workflow) for workflow in workflows_raw.split('\n')]
  return {wf.name: wf for wf in workflows}, [parse_part(part) for part in parts_raw.split('\n')]


def final_state(part: Part, workflows: dict[str, Workflow]) -> bool:
  current = workflows['in']
  while True:
    result = current.evaluate(part)
    if result in {ACCEPT, REJECT}: return result == ACCEPT
    current = workflows[result]


def part1(workflows: dict[str, Workflow], parts: list[Part]) -> int:
  total = 0
  for part in parts:
    if final_state(part, workflows):
      total += part['x'] + part['a'] + part['s'] + part['m']
  return total


def part2(workflows: dict[str, Workflow]) -> int:
  accepted = 0
  parts: list[tuple[str, RangePart]] = [('in', RangePart(RatingRange.base_case(), RatingRange.base_case(), RatingRange.base_case(), RatingRange.base_case()))]
  while parts:
    wfkey, part = parts.pop()
    newly_accepted, new_parts = workflows[wfkey].evaluate_range(part)
    accepted += newly_accepted
    parts.extend(new_parts)
  
  return accepted

def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: data = f.read().strip()
    workflows, parts = parse_input(data)
    print(part1(workflows, parts))
    print(part2(workflows))


if __name__ == '__main__':
  main()
