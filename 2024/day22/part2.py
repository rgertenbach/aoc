from collections import deque, Counter

with open("input.txt") as f:
  numbers = [int(x) for x in f.read().strip("\n").split("\n")]

# We work with 23 bits of information
PRUNE_MASK = (1 << 24) - 1

def rng(secret: int):
  secret = (secret ^ (secret << 6)) & PRUNE_MASK
  secret = (secret ^ (secret >> 5)) & PRUNE_MASK
  secret = (secret ^ (secret << 11)) & PRUNE_MASK
  return secret

current = 123

sequences = []

for number in numbers:
  series = []
  seq = deque()
  for _ in range(2000):
    new = rng(number)
    price = new % 10
    change  = price - number % 10
    seq.append(change)
    if len(seq) > 4: seq.popleft()
    if len(seq) == 4: series.append((tuple(seq), price))
    number = new
  sequences.append(series)

def best_for_trader(sequence):
  out = {}
  for seq, price in sequence:
    if seq not in out: out[seq] = price
  return out


best_sequences = [best_for_trader(seq) for seq in sequences]

best_total = Counter()
for sequences in best_sequences:
  for seq, price in sequences.items():
    best_total[seq] += price


print(max(best_total.values()))

# Not 1550
