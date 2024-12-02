from collections import Counter
import re
with open("input.txt") as f:
  records = f.read().strip("\n")

left = []
right = []

for line in records.split("\n"):
  l, r = re.split(r"\s+", line)
  left.append(int(l))
  right.append(int(r))

f = Counter(right)

total = 0
for l in left:
  total += l * f[l]
print(total)
