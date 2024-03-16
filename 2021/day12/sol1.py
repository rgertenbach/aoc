#!/usr/bin/python3

from typing import List, Dict
import sys
from collections import defaultdict

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
      edges[target].append(source)
  return edges

def continue_path(path: Path, edges: Edges) -> List[Path]:
  next_options = edges[path[-1]]  # All
  # Now remove lower case ones we visited already
  next_options = [no for no in next_options if no.isupper() or no not in path]
  for no in next_options:
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
