import moves as m
from functools import cache

with open("input.txt") as f: codes = f.read().strip("\n").split("\n")

# 451143968040770 too high with 27 (makes sense)
# 181745343862050 too low with 26 (weird)
NBOTS = 26

@cache
def arrow_button(src: str, tgt: str, bots: int) -> int:
  if bots == 0: return 1
  return min(arrow_code(path, bots - 1) for path in m.arrow_paths(src, tgt))


@cache
def arrow_code(path: str, bots: int = 0) -> int:
  return sum(arrow_button(p, b, bots) for p, b in zip("A" + path[:-1], path))


def num_button(src: str, tgt: str, bots: int) -> int:
  if bots == 0: return 1
  return min(arrow_code(path, bots - 1) for path in m.numpad_paths(src, tgt))


def num_code(code: str, bots: int) -> int:
  return sum(num_button(p, b, bots) for p, b in zip("A" + code[:-1], code))

def complexity(code: str, bots: int) -> int:
  moves = num_code(code, bots)
  num = int(code.removesuffix("A").lstrip("0"))
  return num * moves

print(sum(complexity(code, NBOTS) for code in codes))


