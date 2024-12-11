def process_stone(stone: int) -> list[int]:
  if stone == 0: return [1]
  s = str(stone)
  if len(s) % 2 == 0:
    return [int(s[:len(s) // 2]), int(s[len(s) // 2:])]
  return [stone * 2024]


def process_stones(stones: list[int]) -> list[int]:
  out = []
  for stone in stones: out.extend(process_stone(stone))
  return out

with open("input.txt") as f:
  stones = [int(x) for x in f.read().strip("\n").split(" ")]

for _ in range(25):
  print(stones)
  stones = process_stones(stones)

print(len(stones))


