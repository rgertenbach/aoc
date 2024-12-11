from functools import cache

@cache
def process_stone(stone: int) -> list[int]:
  if stone == 0: return [1]
  s = str(stone)
  if len(s) % 2 == 0:
    return [int(s[:len(s) // 2]), int(s[len(s) // 2:])]
  return [stone * 2024]

@cache
def process(stone: int, k: int) -> int:
  if k == 0: return 1
  return sum(process(s, k - 1) for s in process_stone(stone))

with open("input.txt") as f:
  stones = [int(x) for x in f.read().strip("\n").split(" ")]

total = 0
for stone in stones:
  total += process(stone, 75)

print(total)


