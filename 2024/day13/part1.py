import re


A_COST = 3
B_COST = 1

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

def cost(a: tuple[int, int], b: tuple[int, int], prize: tuple[int, int]) -> int:
  px, py = prize
  ax, ay = a
  bx, by = b
  cheapest = None
  for na in range(101):
    if ax * na > px: break
    if ay * na > py: break
    if (px - na * ax) % bx == 0 and (py - na * ay) % by == 0 :
        
        nb = (px - na * ax) // bx
        nb2 = (py - na * ay) // by
        if nb != nb2: continue
        if cheapest is None or na * A_COST + nb * B_COST < cheapest:
          print(prize, na, nb)
          cheapest = na * A_COST + nb * B_COST

  return cheapest or 0


with open("input.txt") as f:
  machines = f.read().strip("\n").split("\n\n")


print(sum(cost(*parse_machine(machine))for machine in machines))
