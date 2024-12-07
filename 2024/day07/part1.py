import itertools
def parse_equation(line: str):
  test_value, parts = line.split(": ")
  return int(test_value), [(x) for x in parts.split(" ")]

def is_valid(test_value: int, parts: list) -> bool:
  ops = [["*", "+"] for _ in range(len(parts)-1)]
  parts = [int(x) for x in parts]
  for setup in itertools.product(*ops):
    # if eval("{}".join(parts).format(*setup)) == test_value:
    #   print(setup)
    #   return True
    res = parts[0]
    for p, op in zip(parts[1:], setup):
      if op == "+": res += p
      else: res *= p
    if res == test_value: return True
  return False

with open("input.txt") as f:
  equations = [parse_equation(line) for line in f.read().strip("\n").split("\n")]

total = 0
for tv, p in equations:
  if is_valid(tv, p):
    total += tv
print(total)
