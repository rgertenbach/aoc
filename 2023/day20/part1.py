import sys
import modules
from collections import deque


def one_pulse(mods: dict[str, modules.Module]) -> tuple[int, int]:
  broadcaster = mods['broadcaster']
  pulses = deque(broadcaster.activate(modules.BUTTON_PULSE))
  low = 1
  high = 0
  while pulses:
    delivery: modules.Delivery = pulses.popleft()
    if delivery.pulse.pulse is modules.Pulse.HIGH: high += 1
    else: low += 1
    if delivery.dest in mods:
      pulses.extend(mods[delivery.dest].activate(delivery.pulse))
  return low, high


def part1(mods: dict[str, modules.Module]) -> int:
  low, high = 0, 0
  for _ in range(1_000):
    lo, hi = one_pulse(mods)
    low += lo
    high += hi

  return low * high


def update_conjunctions(mods: dict[str, modules.Module]) -> None:
  cons = [k for k, v in mods.items() if isinstance(v, modules.Conjunction)]
  for con in cons:
    for input, module in mods.items():
      if con in module.dests:
        mods[con].add(input)



def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f: modules_raw = f.read().strip().split('\n')
    module_list = [modules.parse_module(s) for s in modules_raw]
    mods = {module.name: module for module in module_list}
    update_conjunctions(mods)
    print(part1(mods))
    print()



if __name__ == '__main__':
  main()
  

# High pulse or low pulse sent to each module in list of destination modules

# Modules
# - Flip Flop (%) can be on or off, start as off, high is ignored, low flips (on = high, off=low)
# - Conjunction (&) remember last pulse from each input module, starting with low. When it re
