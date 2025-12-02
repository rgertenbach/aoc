import sys


with open(sys.argv[1]) as f:
    lines = f.read().strip("\n").split("\n")
    instructions = [(line[0], int(line[1:])) for line in lines]

current = 50
zero_any = 0
zero_finish = 0

for d, a in instructions:
    zero_any += a // 100
    a %= 100
    if not a:
        ...
    if d == "L":
        if current and current - a <= 0:
            zero_any += 1
        current -= a
    elif d == "R":
        if current + a > 99:
            zero_any += 1
        current += a
    else:
        raise ValueError(f"Unsupported move {d}")
    current = (current + 100) % 100
    zero_finish += current == 0

print(f"Part 1: {zero_finish}")
print(f"Part 2: {zero_any}")
