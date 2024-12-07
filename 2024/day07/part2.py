import itertools
def parse_equation(line: str):
  test_value, parts = line.split(": ")
  return int(test_value), [int(x) for x in parts.split(" ")]

def is_valid(test_value: int, parts: list[int]) -> bool:
  ops = [["*", "+", "||"] for _ in range(len(parts)-1)]
  for setup in itertools.product(*ops):
    res = parts[0]
    for p, op in zip(parts[1:], setup):
      if op == "+": res += p
      elif op == "||": res = int(f"{res}{p}")
      else: res *= p
    if res == test_value: return True
  return False

with open("input.txt") as f:
  equations = [parse_equation(line) for line in f.read().strip("\n").split("\n")]

total = 0
for i, (tv, p) in enumerate(equations):
  print(f"{i} / {len(equations)}")
  if is_valid(tv, p):
    total += tv
print(total)
