import re
with open("input.txt") as f: memory = f.read()
print(sum(int(l) * int(r) for l, r in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", memory)))

