from collections import defaultdict


network = defaultdict(set)
with open("input.txt") as f:
  for line in f.read().strip("\n").split("\n"):
    l, r = line.split("-")
    network[l].add(r)
    network[r].add(l)

def sets_of_three(network) -> set[frozenset]:
  out = set()
  for n1, conn in network.items():
    for n2 in conn:
      for n3 in conn:
        if n2 == n3: continue
        if n3 not in network[n2]: continue
        out.add(frozenset([n1, n2, n3]))
  return out





triples = sets_of_three(network)
out = 0
for triple in triples:
  out += any(n.startswith("t") for n in triple)
print(out)

