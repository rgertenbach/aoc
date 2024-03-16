import sys
import modules
from collections import deque
import math

RX = 'rx'
CL = 'cl'


def one_pulse(mods: dict[str, modules.Module]) -> str | None:
  broadcaster = mods['broadcaster']
  pulses = deque(broadcaster.activate(modules.BUTTON_PULSE))
  activated = None
  while pulses:
    delivery: modules.Delivery = pulses.popleft()
    if delivery.dest == CL and delivery.idpulse.pulse is modules.Pulse.HIGH:
      if activated is not None: print('conflict')
      activated = delivery.idpulse.src
    if delivery.dest in mods:
      pulses.extend(mods[delivery.dest].activate(delivery.idpulse))
  if any(p is modules.Pulse.HIGH for p in mods[CL].last_pulses.values()):
    print('aad')
  return activated


def part2(mods: dict[str, modules.Module]) -> int:
  rounds = 0
  phase = {}
  for _ in range(10000):
    activated = one_pulse(mods)
    if activated is not None:
      if activated not in phase:
        phase[activated] = rounds + 1
    rounds += 1
  print(phase)
  return math.lcm(*list(phase.values()))


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

