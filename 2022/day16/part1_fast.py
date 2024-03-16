import time
from valve import Valve, System
from valve import load, find_valve
from valve import system_open_valve
from valve import flatten_graph

CYCLES = 30
State = tuple[Valve, int, System, int]
Cache = dict[State, int]


def terminal_flow(valve: Valve, open_cycle: int) -> int:
  return valve.flow * max(0, CYCLES - open_cycle - 1)

def best_flow(
    current: Valve, cycle: int, system: System, cache: Cache, trend: int = 0
) -> int:
  if cycle + 2 >= CYCLES:  # I'd need 1 move to walk, 1 to open
    return trend
  if (key := (current, cycle, system, trend)) in cache:
    return cache[key]
  best = trend
  for dest, steps in current.dests:
    if cycle + steps + 1 >= CYCLES:
      continue
    new_system, new_valve, already_open = system_open_valve(system, dest)
    if not already_open:
      best = max(
          best, 
          best_flow(
            new_valve, cycle + steps + 1, new_system, 
            cache, trend + terminal_flow(new_valve, cycle + steps)))

  cache[key] = best
  return cache[key]


def max_flow(filename: str) -> int:
  start = time.time()
  valves = flatten_graph(load(filename))
  current = find_valve(valves, 'AA')
  result = best_flow(current, 0, valves, {})
  print(f'Took {(time.time() - start)*1000:.1f} ms')
  return result


def main():
  test = max_flow('test_input.txt')
  print(f'{test}', 'Passed!' if test == 1651 else 'Failed!')
  test = max_flow('input.txt')
  print(f'{test}', 'Passed!' if test == 1376 else 'Failed!')
  # 1605 is wrong


if __name__ == '__main__':
  main()

