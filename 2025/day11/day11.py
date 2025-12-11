import sys
from collections import defaultdict, Counter

YOU = "you"
OUT = "out"
SVR = "svr"


def parse_server(s: str) -> tuple[str, set[str]]:
    dev, conn = s.split(": ")
    return dev, set(conn.split(" "))


connections = defaultdict(set)

with open(sys.argv[1]) as f:
    for line in f.read().strip().split("\n"):
        dev, conns = parse_server(line)
        connections[dev] = conns

current = Counter([YOU])
while len(current.keys()) > 1 or YOU in current:
    nxt = Counter()
    for c, n in current.items():
        if c == OUT: nxt[OUT] = n
        for d in connections[c]:
            nxt[d] += n
    current = nxt

print(f"Part 1: {current[OUT]}")

current = Counter([(SVR, False, False)])
while any(c != OUT for c, _, _ in current.keys()):
    nxt = Counter()
    for (c, fft, dac), n in current.items():
        if c == OUT: nxt[(OUT, fft, dac)] += n
        for d in connections[c]:
            is_fft = d == "fft"
            is_dac = d == "dac"
            nxt[(d, fft or is_fft, dac or is_dac)] += n
    current = nxt

print(f"Part 2: {current[(OUT, True, True)]}")

