#!/usr/bin/python3

from typing import List, Dict
import sys
from collections import defaultdict, Counter

START = 'start'
END = 'end'
Point = str
Path = List[Point]
Edges = Dict[Point, List[Point]]


def read_file(filename) -> Edges:
  edges = defaultdict(list)

  with open(filename) as f:
    for line in f:
      source, target = line.strip().split('-')
      edges[source].append(target)
      if source != START and target != END:  
        edges[target].append(source)
  return edges


def continue_path(path: Path, edges: Edges) -> List[Path]:
  nsmol = Counter(point for point in path if point.islower())
  max_nsmol = nsmol.most_common(1)[0][1]
  next_options = edges[path[-1]]
  for no in next_options:
    if no.isupper() or max_nsmol == 1 or no not in path:
      yield path + [no]

def continue_paths(paths: List[Path], edges: Edges):
  for path in paths:
    if path[-1] == END:
      yield path
    else:
      yield from continue_path(path, edges)

edges = read_file(sys.argv[1])
paths = [[START]]

while any(path[-1] != END for path in paths):
  paths = list(continue_paths(paths, edges))
    
print(len(list(paths)))
