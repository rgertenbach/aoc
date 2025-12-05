import sys

with open(sys.argv[1]) as f:
    fresh, ingredients = f.read().strip().split("\n\n")

ingredients = [int(x) for x in ingredients.split("\n")]
fresh = [
    tuple([int(x) for x in f.split("-")])
    for f in fresh.split("\n")
]

def is_fresh(x: int, fresh: list[tuple[int, int]]):
    for s, e in fresh:
        if s <= x <= e: return True
    return False


fresh.sort()

unique_ranges = []
current_start = None
current_end = None

for start, end in fresh:
    if current_end and start > current_end:
        unique_ranges.append((current_start, current_end))
        current_start = start
        current_end = end
    current_end = max(current_end or 0, end)
    if current_start is None:
        current_start = start
unique_ranges.append((current_start, current_end))

part1 = sum(is_fresh(x, unique_ranges) for x in ingredients)
print(f"{part1 = }")
part2 = sum(e - s + 1 for s, e in unique_ranges)
print(f"{part2 = }")

