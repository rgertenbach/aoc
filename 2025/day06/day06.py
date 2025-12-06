import sys
import re
import math

def split_line(line: str, lengths: list[int]) -> list[str]:
    out = []
    start = 0
    for l in lengths:
        out.append(line[start:start + l])
        start += l + 1
    return out

with open(sys.argv[1]) as f:
    *lines, operations = f.read().strip("\n").split("\n")

operations = re.split(r"\s(?=[*+])", operations)

column_widths = [len(x) for x in operations]
operations = [x.strip() for x in operations]

lines = [split_line(line, column_widths) for line in lines]
part1 = 0
part2 = 0

for *parts, op in zip(*lines, operations):
    print(parts)
    normal_parts = [int(x.strip()) for x in parts]
    transformed_parts = [0] * len(parts[0])

    for p in parts[:]:
        for i, d in enumerate(p):
            if d == " ":
                continue
            transformed_parts[i] *= 10
            transformed_parts[i] += int(d)

    if op.strip() == "*":
        part1 += math.prod(normal_parts)
        part2 += math.prod(transformed_parts)
        print(f"* {normal_parts} = {math.prod(normal_parts)}")
        print(f"* {transformed_parts} = {math.prod(transformed_parts)}")
    else:
        part1 += sum(normal_parts)
        part2 += sum(transformed_parts)
        print(f"* {normal_parts} = {sum(normal_parts)}")
        print(f"* {transformed_parts} = {sum(transformed_parts)}")


print(part1)
print(part2)
