from typing import cast
import sys

type Point = tuple[int, int]
type Edge = tuple[Point, Point]


def area_if_filled(
    x1: int, y1: int, x2: int, y2: int, edges: list[Edge]
) -> int:
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)
    for (ex1, ey1), (ex2, ey2) in edges:
        ex1, ex2 = min(ex1, ex2), max(ex1, ex2)
        ey1, ey2 = min(ey1, ey2), max(ey1, ey2)
        if ex2 <= x1 or ex1 >= x2: continue
        if ey2 <= y1 or ey1 >= y2: continue
        return 0
    return (x2 - x1 + 1) * (y2 - y1 + 1)


with open(sys.argv[1]) as f:
    points = [
        cast(Point, tuple([int(x) for x in line.split(",")]))
        for line in f.read().strip().split("\n")
    ]

last_point = points[-1]
edges: list[Edge] = []
for point in points:
    edges.append((last_point, point))
    last_point = point

part1 = 0
part2 = 0
for x1, y1 in points:
    for x2, y2 in points:
        part1 = max(part1, abs((x1 - x2 + 1) * (y1 - y2 + 1)))
        part2 = max(part2, area_if_filled(x1, y1, x2, y2, edges))

print(f"Part 1: {part1}\nPart2: {part2}")
