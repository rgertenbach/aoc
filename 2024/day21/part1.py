import moves
from functools import cache

with open("input.txt") as f:
  codes = f.read().strip("\n").split("\n")


@cache
def numpad_paths(src: str, tgt: str) -> frozenset[str]:
  presses = moves.NUMPAD_PRESSES[src][tgt]
  out = set()
  # vertical first
  if presses[moves.U]:
    out.add(presses[moves.U] * moves.U + presses[moves.L] * moves.L + presses[moves.R] * moves.R + "A")
  elif presses[moves.D] and not (src in "147" and tgt in "0A"):
    out.add(presses[moves.D] * moves.D + presses[moves.L] * moves.L + presses[moves.R] * moves.R + "A")
  elif not presses[moves.D]:
    out.add(presses[moves.L] * moves.L + presses[moves.R] * moves.R + "A")

  # Horizontal first
  if presses[moves.R]:
    out.add(presses[moves.R] * moves.R + presses[moves.U] * moves.U + presses[moves.D] * moves.D + "A")
  elif presses[moves.L] and not (src in "0A" and tgt in "147"):
    out.add(presses[moves.L] * moves.L + presses[moves.U] * moves.U + presses[moves.D] * moves.D + "A")
  elif not presses[moves.L]:
    out.add(presses[moves.U] * moves.U + presses[moves.D] * moves.D + "A")
  return frozenset(out)

@cache
def arrow_paths(src: str, tgt: str) -> frozenset[str]:
  presses = moves.ARROW_PRESSES[src][tgt]
  out = set()
  # vertical first
  if presses[moves.D]:
    out.add(presses[moves.D] * moves.D + presses[moves.L] * moves.L + presses[moves.R] * moves.R + "A")
  elif presses[moves.U] and not (src != "<" and tgt in "^A"):
    out.add(presses[moves.U] * moves.U + presses[moves.L] * moves.L + presses[moves.R] * moves.R + "A")
  elif not presses[moves.U]:
    out.add(presses[moves.L] * moves.L + presses[moves.R] * moves.R + "A")

  # Horizontal first
  if presses[moves.R]:
    out.add(presses[moves.R] * moves.R + presses[moves.U] * moves.U + presses[moves.D] * moves.D + "A")
  elif presses[moves.L] and not (src in "^A" and tgt == "<"):
    out.add(presses[moves.L] * moves.L + presses[moves.U] * moves.U + presses[moves.D] * moves.D + "A")
  elif not presses[moves.L]:
    out.add(presses[moves.U] * moves.U + presses[moves.D] * moves.D + "A")
  return frozenset(out)



@cache
def presses_for_arrow(src: str, tgt: str, robots: int) -> int:
  if robots <= 1: return 1
  return min(arrowpad_code_cost(path, robots - 1) for path in arrow_paths(src, tgt))

@cache
def arrowpad_code_cost(path: str, robots: int = 0) -> int:
  current = "A"
  out = 0
  for b in path:
    out += presses_for_arrow(current, b, robots)
    current = b
  return out



@cache
def presses_for_numpad(src: str, tgt: str, robots: int) -> int:
  return min(arrowpad_code_cost(path, robots) for path in numpad_paths(src, tgt))


def numpad_code_cost(code, robots):
  out = 0
  current = "A"
  for c in code: 
    out += presses_for_numpad(current, c, robots)
    current = c
  return out


total = 0
for code in codes:
  cost = numpad_code_cost(code, 3)
  print(f"{code}: {cost}")
  total += cost * int(code.removesuffix("A").lstrip("0"))

print(total)
