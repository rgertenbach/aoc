import collections
import sys

with open(sys.argv[1]) as f:
    grid = f.read().strip("\n").split("\n")

current = collections.Counter([grid[0].index("S") ])
total_splits = 0

for line in grid[1:]:
    following = collections.Counter()
    splits = 0
    for i, x in enumerate(line):
        if i not in current: continue
        if x == '^':
            splits += 1
            if i: following[(i - 1)] += current[i]
            if i < len(line) - 1: following[(i + 1)] += current[i]
        else:
            following[i] += current[i]
    total_splits += splits
    current = following

print(f"Part 1: {total_splits}")
print(f"Part 2: {sum(current.values())}")

