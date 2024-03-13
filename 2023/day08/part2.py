import sys
import itertools
import sympy
from collections import Counter

from typing import NamedTuple

class Node(NamedTuple):
  name: str
  left: str
  right: str

def parse_node(s: str) -> Node:
  name, nodes_raw = s.split(' = ')
  l, r = nodes_raw.strip('()').split(', ')
  return Node(name, l, r)

def parse(s: str) -> tuple[str, dict[str, Node]]:
  instructions, nodes_raw = s.split('\n\n')
  nodes = [parse_node(node_raw) for node_raw in nodes_raw.split('\n')]
  return instructions, {node.name: node for node in nodes}

def follow(current: str, dir: str, nodes: dict[str, Node]) -> str:
  if dir == 'L': return nodes[current].left
  return nodes[current].right

def cycle(instructions: str, nodes: dict[str, Node], current: str) -> int:
  steps = 0
  for dir in itertools.cycle(instructions):
    # cycles start back at the start
    if current.endswith('Z'): break
    current = follow(current, dir, nodes)
    steps += 1
  return steps


def part2(instructions: str, nodemap: dict[str, Node]) -> None:
  "Relies on the fact that only one suffix node is ever visited"
  starts = [node for node in nodemap.keys() if node.endswith('A')]
  steps = [cycle(instructions, nodemap, node) for node in starts]
  prime_factors = [Counter(sympy.ntheory.primefactors(number)) for number in steps]
  lcm_prime_factors = Counter()
  for factors in prime_factors:
    for factor, freq in factors.items():
      if lcm_prime_factors[factor] < freq: lcm_prime_factors[factor] = freq
  out = 1
  for factor, times in lcm_prime_factors.items():
    out *= factor * times

  return out
  

def main():
  for filename in sys.argv[1:]:
    with open(filename) as f:
      data = f.read().strip()
    instructions, nodes = parse(data)
    print(part2(instructions, nodes))
    print()
    


if __name__ == '__main__':
  main()
