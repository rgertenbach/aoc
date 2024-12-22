with open("input.txt") as f:
  numbers = [int(x) for x in f.read().strip("\n").split("\n")]

# We work with 23 bits of information
PRUNE_MASK = (1 << 24) - 1
print(numbers)

def rng(secret: int):
  secret = (secret ^ (secret << 6)) & PRUNE_MASK
  secret = (secret ^ (secret >> 5)) & PRUNE_MASK
  secret = (secret ^ (secret << 11)) & PRUNE_MASK
  return secret

def nth(secret: int, n: int) -> int:
  for _ in range(n):
    secret = rng(secret)
  return secret

total = 0
for number in numbers: 
  x = nth(number, 2000)
  total += x
print(total)
