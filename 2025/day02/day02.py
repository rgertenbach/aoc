import sys

def repeats(s: str) -> bool:
    n = len(s)
    for l in range(1, n // 2 + 1):
        if n % l: continue
        k = n // l
        if s == k * s[:l]: return True
    return False

def doubles(s: str) -> bool:
    n = len(s)
    if n % 2: return False
    return s[: n // 2] == s[n // 2:]




product_ids = [tuple(x.split("-")) for x in sys.argv[1].strip().split(",")]
part1 = set()
part2 = set()

for start, end in product_ids:
    for x in range(int(start), int(end) + 1):
        if doubles(str(x)): part1.add(x)
        if repeats(str(x)): part2.add(x)

print(f"{sum(part1)=}")
print(f"{sum(part2)=}")
