import sys
import math
import functools

type Point = tuple[int, int, int]
type Edge = tuple[Point, Point]
type Network = set[Point]


def parse_point(s: str) -> Point:
    x, y, z = s.split(",")
    return int(x), int(y), int(z)


def l2(edge: Edge) -> int:
    (x1, y1, z1), (x2, y2, z2) = edge
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2


with open(sys.argv[1]) as f:
    boxes = [parse_point(line) for line in f.read().strip().split("\n")]


distances = sorted(
    [(b1, b2) for b1 in boxes for b2 in boxes if b2 < b1], reverse=True, key=l2
)

networks = [set(distances.pop()) for _ in range(int(sys.argv[2]))]


def union_find_one_round(networks: list[Network]) -> list[Network]:
    new_networks = []
    while networks:
        candidate = networks.pop()
        for already_processed in new_networks:
            if already_processed & candidate:
                already_processed |= candidate
                return new_networks + networks
        new_networks.append(candidate)
    return new_networks


def union_find(networks: list[Network]) -> list[Network]:
    old_l = len(networks)
    while True:
        networks = union_find_one_round(networks)
        l = len(networks)
        if l == old_l:
            break
        old_l = l
    return networks


networks = union_find(networks)
sizes = sorted([len(x) for x in networks])
print(f"Part 1: {math.prod(sizes[-3:])}")

e = None
while len(networks[0]) < len(boxes):
    e = distances.pop()
    networks.append(set(e))
    networks = union_find(networks)


assert e is not None

print(f"Part 2: {e[0][0] * e[1][0]} ({e})")
