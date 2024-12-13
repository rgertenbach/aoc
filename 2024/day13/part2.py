import re
import z3


A_COST = 3
B_COST = 1
OFFSET = 10000000000000

def parse_machine(s: str) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
  a, b, c = s.split("\n")
  a = re.match(r".*X\+(\d+), Y\+(\d+)$", a)
  b = re.match(r".*X\+(\d+), Y\+(\d+)$", b)
  c = re.match(r"Prize: X=(\d+), Y=(\d+)$", c)
  if a is None: raise ValueError(a)
  if b is None: raise ValueError(b)
  if c is None: raise ValueError(c)
  return (
      (int(a.group(1)), int(a.group(2))),
      (int(b.group(1)), int(b.group(2))),
      (int(c.group(1)), int(c.group(2)))
  )

def cost(a: tuple[int, int], b: tuple[int, int], prize: tuple[int, int]):
  na, nb = z3.Int("na"), z3.Int("nb")
  ax, bx, ay, by = z3.Int("ax"), z3.Int("bx"), z3.Int("ay"), z3.Int("by")
  px, py = z3.Int("px"), z3.Int("py")

  s = z3.Solver()
  s.add(
    ax == a[0], ay == a[1],
    bx == b[0], by == b[1],
    px == prize[0] + OFFSET, py == prize[1] + OFFSET,
    na >= 0, nb >= 0,
    na * ax == px - nb * bx,
    na * ay == py - nb * by
  )
  if s.check() != z3.sat: return 0
  m = s.model()

  return m.evaluate(na).as_long() * A_COST+  m.evaluate(nb).as_long() * B_COST


with open("input.txt") as f:
  machines = f.read().strip("\n").split("\n\n")


total = 0
for machine in machines:
  a,b, c = parse_machine(machine)
  total += cost(a, b, c)
print(total)
