from collections import defaultdict, Counter
import sys
from typing import DefaultDict
import random

Graph = DefaultDict[str, set[str]]

def parse_line(s: str) -> list[tuple[str, str]]:
  lhs, rhs = s.split(': ')
  dests = rhs.split(' ')
  out = []
  for dest in dests:
    out.append((lhs, dest))
    out.append((dest, lhs))
  return out


def parse_graph(s: str) -> Graph:
  out = defaultdict(set)
  for line in s.split('\n'):
    for n1, n2 in parse_line(line):
      out[n1].add(n2)
      out[n2].add(n1)
  return out


def bfs(graph: Graph, src: str, dest: str) -> list[str]:
  visited = set()
  queue = [(src, [])]
  while queue:
    next_queue = []
    for current, path in queue:
      if current in visited: continue
      path = path[:]
      visited.add(current)
      if current == dest: return path
      path.append(current)
      for d in graph[current]: next_queue.append((d, path.copy()))
    queue = next_queue
  return []



def bfs_paths(graph: Graph, src: str, dst: str) -> list[list[tuple[str, str]]]:
  visited = set()
  frontier = [(src, [])]
  out: list[list[tuple[str, str]]] = []
  while frontier:
    next_frontier = []
    for current_node, current_path in frontier:
      if current_node == dst:
        out.append(current_path)
        return out
        continue
      if current_node in visited: continue
      visited.add(current_node)
      for next_node in graph[current_node]:
        next_frontier.append(
            (next_node, current_path + [(min(current_node, next_node), max(current_node, next_node))]))
    frontier = next_frontier
  # No connection
  return out


def random_edge_importance(graph: Graph, n: int) -> Counter[tuple[str, str]]:
  importances = Counter()
  nodes = list(graph.keys())
  for _ in range(n):
    n1 = random.choice(nodes)
    n2 = random.choice(nodes)
    if n1 == n2: continue
    paths = bfs_paths(graph, min(n1, n2), max(n1, n2))
    if paths:
      for path in paths:
        for edge in path:
          importances[edge] += 1

  return importances

def subgraph_sizes(graph: Graph, cut: set[tuple[str, str]]) -> list[int]:
  sizes = []
  nodes = list(graph.keys())
  visited = set()
  for node in nodes:
    if node in visited: continue
    size = 0
    stack = [node]
    while stack:
      current = stack.pop()
      if current in visited: continue
      visited.add(current)
      size += 1
      for dest in graph[current]:
        edge = min(current, dest), max(current, dest)
        if dest not in visited and edge not in cut:
          stack.append(dest)
    sizes.append(size)
  return sizes


def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: data = f.read().strip()
    conns = parse_graph(data)
    importances = random_edge_importance(conns, 10_000).most_common(3)
    print(importances)
    sizes = subgraph_sizes(conns, set(edge for edge, _ in importances))
    print(sizes)
    print(sizes[0] * sizes[1])


if __name__ == '__main__':
  main()
