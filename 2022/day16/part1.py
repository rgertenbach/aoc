import re
from collections import namedtuple

CYCLES = 30
Valve = namedtuple('Valve', ['name', 'flow', 'dests', 'is_open'])
System = tuple[Valve, ...]
CacheKey = tuple[Valve, int, System]
Cache = dict[CacheKey, int]


def parse_valve(s: str) -> Valve:
  pat = r'Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (.*)'
  m = re.match(pat, s)
  if m is not None:
    name, flow, dests = m.group(1, 2, 3)
    # So we don't try opening 0 flow valves
    return Valve(name, int(flow), tuple(dests.split(', ')), int(flow) == 0)
  raise ValueError(f'Row cannot be parsed: "{s}"')


def load(filename: str) -> System:
  with open(filename) as f:
    valves = f.read().strip().split('\n')
  return tuple(parse_valve(v) for v in valves)


def one_flow(valves: System) -> int:
  return sum(v.flow for v in valves if v.is_open)


def find_valve(system: System, name: str) -> Valve:
  for v in system:
    if v.name == name:
      return v
  raise RuntimeError(f'{name} not found in system')


def try_open_valve(valve: Valve) -> Valve:
  if valve.is_open:
    raise RuntimeError(f'{valve.name} is already open!')
  return Valve(valve.name, valve.flow, valve.dests, True)


def open_valve(system: System, name: str) -> System:
  return tuple(try_open_valve(v) if v.name == name else v for v in system)


def best_flow(current: Valve, cycle: int, system: System, cache: Cache) -> int:
  if cycle >= CYCLES:
    return 0
  key = (current, cycle, system)
  if key in cache:
    return cache[key]

  best = 0
  flow = one_flow(system)

  for dest in current.dests:
    attempt = flow + best_flow(find_valve(system, dest), cycle + 1, system, cache)
    if attempt > best:
      best = attempt
    if current.is_open:
      continue
    sys_after_open = open_valve(system, current.name)
    opened_valve = find_valve(sys_after_open, current.name)
    attempt = flow + best_flow(opened_valve, cycle + 1, sys_after_open, cache)
    if attempt > best:
      best = attempt

  cache[key] = best

  return cache[key]


def max_flow(filename: str) -> int:
  valves = load(filename)
  start_valve = [v for v in valves if v.name == 'AA'][0]
  cache = {}  # (Valve, cycle, state) -> int
  return best_flow(start_valve, 0, valves, cache)


def main():
  print('Test')
  test = max_flow('test_input.txt')
  print(f'{test=}', 'Passed!' if test == 1651 else 'Failed!')

  print(max_flow('input.txt'))


if __name__ == '__main__':
  main()
