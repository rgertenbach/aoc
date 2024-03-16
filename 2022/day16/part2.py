import itertools
import math
import time
from valve import Valve, System
from valve import load, find_valve
from valve import system_open_valve
from valve import flatten_graph

CYCLES = 26
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
  result = combos(valves)
  print(f'Took {(time.time() - start)*1000:.1f} ms')
  return result


def tv(path: tuple[str],
       terminal: dict[tuple[str, int], int],
       distances: dict[str, dict[str, int]]) -> int:
  cycle = 0
  total = 0
  current = 'AA'
  for dest in path:
    cycle += distances[current][dest] + 1
    if cycle >= CYCLES:
      break
    total += terminal[dest, CYCLES - cycle ]
    current = dest
  return total


def best_of_permutation(grp1: set[str], 
                        grp2: set[str], 
                        terminal: dict[tuple[str, int], int],
                        distances: dict[str, dict[str, int]]) -> int:
  best = 0
  grp1_permutations = math.factorial(len(grp1))
  tv1s = [tv(perm, terminal, distances) for perm in itertools.permutations(grp1)]
  tv2s = [tv(perm, terminal, distances) for perm in itertools.permutations(grp2)]
  return max(tv1s) + max(tv2s)

  return best, best_path


def combos(system: System) -> int:
  best = 0
  terminal_values = {}
  for n_cycles in range(CYCLES):
    for valve in system:
      terminal_values[(valve.name, n_cycles)] = valve.flow * n_cycles
  nodes = set([valve.name for valve in system if valve.name != 'AA'])
  distances = {valve.name: {dest: dist for dest, dist in valve.dests} for valve in system}
  
  for i, grp1 in enumerate(itertools.combinations(nodes, len(nodes) // 2)):
    print(f'Doing combination {i} of {math.comb(len(nodes), len(nodes) // 2)}')
    grp2 = nodes.difference(grp1)
    attempt = best_of_permutation(grp1, grp2, terminal_values, distances)
    if attempt > best:
      best = attempt
  return best


def main():
  test = max_flow('test_input.txt')
  # print(f'{test}', 'Passed!' if test == 1707 else 'Failed!')
  test = max_flow('input.txt')
  print(f'{test}', 'Passed!' if test == 920 else 'Failed!')
  # 1605 is wrong


if __name__ == '__main__':
  main()



