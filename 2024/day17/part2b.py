import heapq
import re
from collections import Counter
# An attempt to do it smarter that gets stuck somewhere, cannot be bothered to debug

AREG = 4

def combo(x, a, b, c) -> int:
  if x == 7: raise RuntimeError("7 is an Invalid opcode")
  return {AREG: a, 5: b, 6: c}.get(x, x)

def format(xs): return ",".join([str(x) for x in xs])

def bin_prefix(orig_a: str, prefix: int) -> tuple[int, str]:
  new_a = f"{prefix:03b}{orig_a}"
  return int(new_a, 2), new_a

with open("test_input3.txt") as f:
# with open("input.txt") as f:
  registers, sprogram = f.read().strip("\n").split("\n\n")

# Need to debug 2 and 7

orig_b, orig_c = [
    int(re.findall(r"Register \w: (.*)", r)[0])
    for r in registers.split("\n")[1:]
]
program = [int(x) for x in sprogram.removeprefix("Program: ").split(",")]

def push_if_not_in(heap, a):
  if any((a[1] == x[1] for x in heap)): return
  heapq.heappush(heap, a)

heap: list[tuple[int | None, str]] = [(None, "")]
cnt = Counter()
while heap:
  a, orig_a = heapq.heappop(heap)
  b, c = orig_b, orig_c
  p = 0
  out = []
  restart = False
  total_a_shifts = 0
  print(f"---Restarting with {orig_a=} {a=}---")
  if len(orig_a) > 63: continue
  while len(out) < len(program):
    if p >= len(program) - 1: break
    op, operand = program[p:p+2]
    cnt[op] += 1
    print(f"  {op=} {operand=}, {a=}, {b=}, {c=}")
    if op == 0:
      if operand == AREG: print("Areg as input to ADV")
      if a is None:
        for i in range(8): push_if_not_in(heap, bin_prefix(orig_a, i))
        restart = True
        break
      shifts = combo(operand, a, b, c)
      if shifts != 3: raise RuntimeError("Shift != 3")
      a = a >> shifts
      total_a_shifts += shifts
      if total_a_shifts > len(orig_a) - 3:
        for i in range(8): push_if_not_in(heap, bin_prefix(orig_a, i))
        restart = True
        break
      if total_a_shifts == len(orig_a): a = None

    elif op == 1: b ^= operand
    elif op == 2:
      if operand == AREG and a is None:
        for i in range(8): push_if_not_in(heap, bin_prefix(orig_a, i))
        restart = True
        break
      b = combo(operand, a, b, c) & 7
    elif op == 3:
      if a is None:
        for i in range(8): push_if_not_in(heap, bin_prefix(orig_a, i))
        restart = True
        break
      elif a == 0:
        # print(f"{total_a_shifts} / {len(orig_a)}")
        start = 1 if total_a_shifts < len(orig_a) - 3 else 0
        # print(f"adding from {start}")
        for i in range(start, 8): push_if_not_in(heap, bin_prefix(orig_a, i))
        # restart = True
        # break
      if a: p = operand
    elif op == 4: b ^= c
    elif op == 5:
      if len(out) == len(program):
        restart = True
        break
      if operand == AREG:
        if a is None:
          push_if_not_in(heap, bin_prefix(orig_a, program[len(out)]))
          restart = True
          break
      operand = combo(operand, a, b, c)
      if operand & 7 != program[len(out)]:
        restart = True
        break
      out.append(operand & 7)
    elif op == 6: raise RuntimeError("BDV should not appear")
    elif op == 7:
      if a is None:
        for i in range(8): push_if_not_in(heap, bin_prefix(orig_a, i))
        restart = True
        break
      if total_a_shifts > len(orig_a) - 3:
        for i in range(8): push_if_not_in(heap, bin_prefix(orig_a, i))
        restart = True
        break
      shifts = combo(operand, a, b, c)
      c = a >> shifts
    if restart: continue
    if op != 3 or a == 0: p += 2
  if str(out) == str(program): 
    print(orig_a, int(orig_a, 2))
    break
  # if format(program).startswith(format(out)):
  #   for i in range(8): push_if_not_in(heap, bin_prefix(orig_a, i))

      
for op in range(8):
  print(f"{op}: {cnt[op]}")
# Test  answer
# 11100101011000000
