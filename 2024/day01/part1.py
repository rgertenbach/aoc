import re
with open("input.txt") as f:
  records = f.read().strip("\n")

left = []
right = []

for line in records.split("\n"):
  l, r = re.split(r"\s+", line)
  left.append(int(l))
  right.append(int(r))

left.sort()
right.sort()

total = 0
for l, r in zip(left, right):
  total += abs(l - r)
print(total)
