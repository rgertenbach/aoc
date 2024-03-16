from enum import Enum
import abc
from typing import Iterator, NamedTuple
from collections import defaultdict

class ModuleType(Enum):
  FLIP_FLOP = '%'
  CONJUNCTION = '&'
  BROADCAST = 'broadcaster'

class Pulse(Enum):
  LOW = 'low'
  HIGH = 'high'

class State(Enum):
  OFF = 0
  ON = 1

  def flip(self) -> 'State':
    if self is State.OFF: return State.ON
    return State.OFF

class IdentifiedPulse(NamedTuple):
  src: str
  pulse: Pulse

  def __str__(self) -> str:
    return f'{self.src} -{self.pulse.value}-'

BUTTON_PULSE = IdentifiedPulse('button', Pulse.LOW)

class Delivery(NamedTuple):
  dest: str
  pulse: IdentifiedPulse

  def __str__(self) -> str:
    return f'{self.pulse} > {self.dest}'

class Module(metaclass=abc.ABCMeta):
  def __init__(self, name: str, dests: list[str]) -> None:
    self.name = name
    self.dests = dests


  @abc.abstractmethod
  def activate(self, pulse: IdentifiedPulse) -> Iterator[Delivery]:
    ...

class Broadcaster(Module):
  "Sends a low signal to all destinations"
  def __init__(self, dests: list[str]) -> None:
    super().__init__('broadcaster', dests)

  def activate(self, pulse: IdentifiedPulse) -> Iterator[Delivery]:
    del pulse
    for dest in self.dests:
      yield Delivery(dest, IdentifiedPulse(self.name, Pulse.LOW))

  def __str__(self) -> str:
    return f'Broadcaster {self.name} that sends to {self.dests}'

class FlipFlop(Module):
  "Ignores HIGH, otherwise flips its state and returns HIGH if on else LOW."
  def __init__(self, name: str, dests: list[str]):
    super().__init__(name, dests)
    self.state = State.OFF

  def activate(self, pulse: IdentifiedPulse) -> Iterator[Delivery]:
    if pulse.pulse is Pulse.HIGH: return
    self.state = self.state.flip()
    for dest in self.dests:
      yield Delivery(
          dest, 
          IdentifiedPulse(
            self.name,
            Pulse.HIGH if self.state is State.ON else Pulse.LOW))

  def __str__(self) -> str:
    return f'FlipFlop {self.name} that is {self.state} and sends to {self.dests}'


class Conjunction(Module):
  "Remembers state of last input (defaults to low) pulses LOW if all were HIGH"
  def __init__(self, name: str, dests: list[str]) -> None:
    super().__init__(name, dests)
    self.last_pulses = defaultdict(lambda: Pulse.LOW)

  def activate(self, pulse: IdentifiedPulse) -> Iterator[Delivery]:
    self.last_pulses[pulse.src] = pulse.pulse
    pulse_to_send = Pulse.LOW if self.all_high() else Pulse.HIGH
    for dest in self.dests:
      yield Delivery(dest, IdentifiedPulse(self.name, pulse_to_send))

  def all_high(self) -> bool:
    return all(p is Pulse.HIGH for p in self.last_pulses.values())

  def __str__(self) -> str:
    return f'Conjunction {self.name} that remembers {self.last_pulses} to {self.dests}'

  def extend(self, inputs: list[str]) -> None:
    for x in inputs:
      self.last_pulses[x] = Pulse.LOW

  def add(self, input: list[str]) -> None:
      self.last_pulses[input] = Pulse.LOW


def parse_module(s: str) -> Module:
  name_raw, pulses_raw = s.split(' -> ')
  pulses = pulses_raw.split(', ')
  if name_raw == 'broadcaster': return Broadcaster(pulses)
  kind = name_raw[0]
  name = name_raw[1:]
  if ModuleType(kind) is ModuleType.FLIP_FLOP: return FlipFlop(name, pulses)
  if ModuleType(kind) is ModuleType.CONJUNCTION: return Conjunction(name, pulses)
  raise RuntimeError(f'Unsupported kind {kind}')

