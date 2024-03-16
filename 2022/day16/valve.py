import re
from collections import namedtuple

Valve = namedtuple('Valve', ['name', 'flow', 'dests', 'is_open'])
Dest = namedtuple('Dest', ['name', 'dist'])
System = tuple[Valve, ...]


# Load Data

def parse_valve(s: str) -> Valve:
  pat = r'Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (.*)'
  m = re.match(pat, s)
  if m is not None:
    name, flow, dests = m.group(1, 2, 3)
    # So we don't try opening 0 flow valves
    dests = tuple(Dest(d, 1) for d in dests.split(', '))
    return Valve(name, int(flow), dests, int(flow) == 0)
  raise ValueError(f'Row cannot be parsed: "{s}"')

def load(filename: str) -> System:
  with open(filename) as f:
    valves = f.read().strip().split('\n')
  return tuple(parse_valve(v) for v in valves)


# Print data
def print_valve(valve: Valve) -> None:
  print(f'{valve.name}: {valve.flow} is', 'open' if valve.is_open else 'shut')
  for dest, cost in valve.dests:
    print(f'\t{dest}\t{cost}')


def print_system(system: System) -> None:
  for valve in system:
    print_valve(valve)


# Interact with data
def find_valve(system: System, name: str) -> Valve:
  for v in system:
    if v.name == name:
      return v
  raise RuntimeError(f'{name} not found in system')


def open_valve(valve: Valve) -> Valve:
  return Valve(valve.name, valve.flow, valve.dests, True)


def system_open_valve(system: System, name: str) -> tuple[System, Valve, bool]:
  new_sys = []
  opened_valve = None
  was_open = None
  for valve in system:
    if valve.name == name:
      was_open = valve.is_open
      opened_valve = valve = open_valve(valve)
    new_sys.append(valve)
  return tuple(new_sys), opened_valve, was_open


# Compress data
def raise_grandchildren(valve: Valve, lookup: dict[str, Valve]) -> Valve:
  out = {}
  dests = valve.dests
  for dest, cost in valve.dests:
    if dest in out:
      out[dest] = min(out[dest], cost)
    else:
      out[dest] = cost
    for gc, extra_cost in lookup[dest].dests:
      if gc in out:
        out[gc] = min(out[gc], cost + extra_cost)
      else:
        out[gc] = cost + extra_cost

  dests = tuple([Dest(d, c) for d, c in out.items()])
  return Valve(valve.name, valve.flow, dests, valve.is_open)


def raise_ancestors(valve: Valve, lookup: dict[str, Valve]) -> Valve:
  while (raised := raise_grandchildren(valve, lookup)) != valve:
    valve = raised
  dests = tuple([dest for dest in valve.dests if lookup[dest.name].flow and dest.name != valve.name])
  return Valve(valve.name, valve.flow, dests, valve.is_open)


def flatten_graph(system: System) -> System:
  m = {v.name: v for v in system}
  raised = [
      raise_ancestors(valve, m) 
      for valve 
      in system 
      if valve.name == 'AA' or valve.flow]
  return tuple(raised)
