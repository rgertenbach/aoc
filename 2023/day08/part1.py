import sys
import itertools

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


def part1(instructions: str, nodemap: dict[str, Node]) -> int:
  steps = 0
  current = 'AAA'
  for dir in itertools.cycle(instructions):
    if dir == 'L': current = nodemap[current].left
    else: current = nodemap[current].right
    steps += 1
    if current == 'ZZZ': break
  return steps

def main():
  for filename in sys.argv[1:]:
    with open(filename) as f:
      data = f.read().strip()
    instructions, nodes = parse(data)
    start = 'AAA'
    print(part1(instructions, nodes))
    


if __name__ == '__main__':
  main()
