import functools
import sys
with open(sys.argv[1]) as f:
    banks = f.read().strip().split("\n")

part1 = 0
part2 = 0

@functools.cache
def max_joltage(s: str, k: int) -> int:
    if k == 0: return 0
    if not s: return 0
    if len(s) < k: return 0
    skip = max_joltage(s[1:], k)
    keep = 10**(k-1) * int(s[0]) + max_joltage(s[1:], k-1)
    return max(skip, keep)


for bank in banks:
    n = len(bank)
    highest_following = [0] * n
    part1 += max_joltage(bank, 2)
    part2 += max_joltage(bank, 12)


print(f"{part1=}")
print(f"{part2=}")
