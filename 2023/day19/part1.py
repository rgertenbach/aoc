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

  @classmethod
  def parse(cls, s: str) -> 'Rule':
    if ':' not in s: return cls(s)
    comp, action = s.split(':')
    mat = re.match(r'([amsx])([<>])(\d+)', s)
    if mat is None: raise RuntimeError(f'Could not parse {s}')
    field, comp, thresh = mat.groups()
    return cls(action, field, Comparison(comp), int(thresh))

  @property
  def is_constant(self) -> bool:
    return self.threshold == 0

  def evaluate(self, part: Part) -> str:
    if self.comp is Comparison.NONE: return self.action
    if self.comp is Comparison.LESS_THAN and part[self.field] < self.threshold: return self.action
    if self.comp is Comparison.GREATER_THAN and part[self.field] > self.threshold: return self.action
    return NONE

class Workflow:
  def __init__(self, name: str, rules: list[Rule]):
    self.name = name
    self.rules = rules

  @classmethod
  def parse(cls, s: str) -> 'Workflow':
    name, rules_s = s.strip(CLOSE).split(OPEN)
    return cls(name, [Rule.parse(rule) for rule in rules_s.split(',')])

  def __str__(self) -> str:
    return f'{self.name}: {self.rules}'

  def evaluate(self, part: Part) -> str:
    for rule in self.rules:
      result = rule.evaluate(part)
      if result != NONE: return result
    raise RuntimeError(f'{self} applied on {part} did not yield any result')


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

def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: data = f.read().strip()
    workflows, parts = parse_input(data)
    print(part1(workflows, parts))


if __name__ == '__main__':
  main()
