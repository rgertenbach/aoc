from collections import defaultdict
import itertools



network = defaultdict(set)
with open("input.txt") as f:
  for line in f.read().strip("\n").split("\n"):
    l, r = line.split("-")
    network[l].add(r)
    network[r].add(l)
    network[l].add(l)
    network[l].add(r)




largest_n = 0
largest = tuple()

maxsize = max(len(e) for e in network.values())

for nodei, (node, edges) in enumerate(network.items()):
  for size in range(largest_n + 1, len(edges) + 1):
    for i, combination in enumerate(itertools.combinations(edges, size)):
      s = set(edges)
      for conn in combination:
        s &= network[conn]
        if len(s) < size: break
      if len(s) >= size:
        largest_n = size
        largest = combination
        break


print(",".join(sorted([*largest]))) 
