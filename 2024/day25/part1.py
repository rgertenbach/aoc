with open("input.txt") as f:
  blocks = [block.split("\n") for block in f.read().strip("\n").split("\n\n")]

locks = []
keys = []

WIDTH = 5
HEIGHT = 6


for block in blocks:
  is_lock = block[0] == "#" * WIDTH and block[-1] == "." * WIDTH
  if is_lock:
    heights = [-1] * WIDTH
    for line in block:
      for i, x in enumerate(line):
        if x == "#": heights[i] += 1
    locks.append(heights)
  else: 
    heights = [HEIGHT] * WIDTH
    for line in block:
      for i, x in enumerate(line):
        if x == ".": heights[i] -= 1
    keys.append(heights)

def overlap(lock, key) -> bool:
  for l, k in zip(lock, key):
    if l + k >= HEIGHT: return True
  return False

fit = 0

for lock in locks:
  for key in keys:
    if not overlap(lock, key):
      fit += 1
    # print(f"{lock=} and {key}: {overlap(lock, key)=}")


print(fit)



