import re
with open("input.txt") as f: memory = f.read()
pattern = r"mul\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don't)\(\)"

matches = re.findall(pattern, memory)
total = 0
enabled = True
for l, r, do, dont in matches:
  if do: enabled = True
  if dont: enabled = False
  if l and enabled:
    total += int(l) * int(r)


print(total)
