import sys
import modules
from collections import deque


def one_pulse(mods: dict[str, modules.Module]) -> bool:
  broadcaster = mods['broadcaster']
  pulses = deque(broadcaster.activate(modules.BUTTON_PULSE))
  while pulses:
    delivery: modules.Delivery = pulses.popleft()
    if delivery.dest == 'rx' and delivery.pulse.pulse is modules.Pulse.LOW:
      return True
    if delivery.dest in mods:
      pulses.extend(mods[delivery.dest].activate(delivery.pulse))
  return False


def part2(mods: dict[str, modules.Module]) -> int:
  rounds = 0
  while True:
    if one_pulse(mods): break
    rounds += 1
    if rounds % 1_000 == 0:
      print('\r  -> ', f'{rounds:,d}', '\r', end='')

  return rounds + 1


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
    print(part2(mods))
    print()



if __name__ == '__main__':
  main()
  

# High pulse or low pulse sent to each module in list of destination modules

# Modules
# - Flip Flop (%) can be on or off, start as off, high is ignored, low flips (on = high, off=low)
# - Conjunction (&) remember last pulse from each input module, starting with low. When it re
