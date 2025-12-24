import sys
import re
import datetime
from typing import NamedTuple


class Manual(NamedTuple):
    indicator: str
    buttons: list[frozenset[int]]
    joltage: list[int]


def parse_machine(s: str):
    match = re.match(r"^\[(.*)\] (\(.*\)) \{(.*)\}$", s)
    if match is None:
        raise ValueError(f"Failed to parse: {s}")
    indicator = match.group(1)
    wirings_match = re.findall(r"\((.*?)\)", match.group(2))
    if wirings_match is None:
        raise ValueError(f"Could not extract wirings from {s}")
    wirings = [frozenset([int(x) for x in w.split(",")]) for w in wirings_match]

    joltage = [int(x) for x in match.group(3).split(",")]
    return Manual(indicator, wirings, joltage)


with open(sys.argv[1]) as f:
    machines = [parse_machine(line) for line in f.read().strip().split("\n")]


def match_indicator(state: list[bool], pattern: str):
    for s, p in zip(state, pattern):
        if s != (p == "#"):
            return False
    return True


def solve_indicator(m: Manual) -> int:
    machines = [[False] * len(m.indicator)]
    steps = 0
    while True:
        next_machines = []
        for machine in machines:
            if match_indicator(machine, m.indicator):
                return steps
            for buttons in m.buttons:
                next_machine = machine[:]
                for button in buttons:
                    next_machine[button] = not next_machine[button]
                next_machines.append(next_machine)
        machines = next_machines
        steps += 1
    return steps


# part1 = 0
# for i, machine in enumerate(machines):
#     print(f"{i} / {len(machines)}")
#     part1 += solve_indicator(machine)
# print(f"Part1: {part1}")


def match_joltage(state: list[int], pattern: list[int]) -> int:
    all_match = True
    for s, p in zip(state, pattern):
        if s > p:
            return 1
        if s < p:
            all_match = False
    if all_match:
        return 0
    return -1


def increase_presses(presses: list[int], limits: list[int]) -> list[int]:
    n = len(presses)
    out = presses[:]
    out[-1] += 1
    check = n - 1
    while check > 0 and out[check] > limits[check]:
        out[check - 1] += 1
        for i in range(check, n):
            out[i] = 0
        check -= 1
    return out

def skip_presses(presses: list[int]) -> list[int]:
    out = presses[:]
    n = len(out)
    i = n - 1
    while i and out[i] == 0: i -= 1
    out[i-1] += 1
    for j in range(i, n):
        out[j] = 0
    return out


def solve_joltage(m: Manual) -> int:
    max_presses = [min(m.joltage[b] for b in buttons) for buttons in m.buttons]
    presses = [0] * len(m.buttons)
    best = 99999999999999999
    while presses[0] <= max_presses[0]:
        machine = [0] * len(m.joltage)
        for buttons, p in zip(m.buttons, presses):
            for d in buttons:
                machine[d] += p
        match = match_joltage(machine, m.joltage)
        if match == 0: best = min(best, sum(presses))
        if match == 1: presses = skip_presses(presses)
        else: presses = increase_presses(presses, max_presses)

   
    print("\r", end="")
    return best



part2 = 0
print(f"{datetime.datetime.now().isoformat()}: Starting")
for i, machine in enumerate(machines):
    part2 += solve_joltage(machine)
    print(f"{datetime.datetime.now().isoformat()}: {i+1} / {len(machines)} ")
print(f"Part2: {part2}")
