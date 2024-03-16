from typing import Iterable, Optional, Iterator, Tuple

import itertools

from cuboid import State, Cuboid, Instruction

Point = Tuple[int, int, int]


class Reactor:
  def __init__(self, cuboids: Optional[Iterable[Cuboid]] = None):
    self.cuboids = list(cuboids if cuboids is not None else [])

  def __len__(self):
    return sum(len(c) for c in self.cuboids)

  @property
  def points(self) -> Iterator[Point]:
    yield from itertools.chain.from_iterable(c.points for c in self.cuboids)

  def __add__(self, c: Cuboid) -> 'Reactor':
    'Turn on a cuboid without changing already turned on ones'
    # For simplicity we first turn off all intersections.
    # We *then* add the new cuboid whole.
    # This seems simpler than the opposite.
    removed = self - c
    return Reactor([c] + removed.cuboids)

  def __sub__(self, c: Cuboid) -> 'Reactor':
    'Turn off a cuboid'
    new = [out for sc in self.cuboids for out in (sc - c)]
    return Reactor(new)



