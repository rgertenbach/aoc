from collections import namedtuple
from collections import Counter

Elf = namedtuple('Elf', ['x', 'y'])
Elves = set[Elf]

def load(filename: str) -> Elves:
    with open(filename) as f:
        rows = f.read().strip().split('\n')
    elves = set()
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            if cell == '#':
                if Elf(x, y) not in elves:
                    elves.add(Elf(x, y))
              
    return elves
    

def all_free(elf: Elf, elves: Elves) -> bool:
  return (
      Elf(elf.x - 1, elf.y - 1) not in elves
      and Elf(elf.x + 0, elf.y - 1) not in elves
      and Elf(elf.x + 1, elf.y - 1) not in elves
      and Elf(elf.x - 1, elf.y + 1) not in elves
      and Elf(elf.x + 0, elf.y + 1) not in elves
      and Elf(elf.x + 1, elf.y + 1) not in elves
      and Elf(elf.x - 1, elf.y + 0) not in elves
      and Elf(elf.x + 1, elf.y + 0) not in elves)


def north_free(elf: Elf, elves: Elves) -> bool:
  return (
      Elf(elf.x - 1, elf.y - 1) not in elves
      and Elf(elf.x + 0, elf.y - 1) not in elves
      and Elf(elf.x + 1, elf.y - 1) not in elves)

def south_free(elf: Elf, elves: Elves) -> bool:
  return (
      Elf(elf.x - 1, elf.y + 1) not in elves
      and Elf(elf.x + 0, elf.y + 1) not in elves
      and Elf(elf.x + 1, elf.y + 1) not in elves)

def west_free(elf: Elf, elves: Elves) -> bool:
  return (
      Elf(elf.x - 1, elf.y + 1) not in elves
      and Elf(elf.x - 1, elf.y + 0) not in elves
      and Elf(elf.x - 1, elf.y - 1) not in elves)

def east_free(elf: Elf, elves: Elves) -> bool:
  return (
      Elf(elf.x + 1, elf.y + 1) not in elves
      and Elf(elf.x + 1, elf.y + 0) not in elves
      and Elf(elf.x + 1, elf.y - 1) not in elves)

      
def propose_move_for(elf: Elf, elves: Elves, step: int) -> Elf:
    fns = [(north_free, 'N'), (south_free, 'S'), (west_free, 'W'), (east_free, 'E')]
    idx = step % len(fns)
    fns = fns[idx:] + fns[:idx]
    if all_free(elf, elves):
      return elf
    for fn, direction in fns:
        is_free = fn(elf, elves)
        if not is_free:
          continue
        if direction == 'N':
            return Elf(elf.x, elf.y - 1)
        if direction == 'S':
            return Elf(elf.x, elf.y + 1)
        if direction == 'W':
            return Elf(elf.x - 1, elf.y)
        if direction == 'E':
            return Elf(elf.x + 1, elf.y)
    return elf
  
    
def move(elves: Elves, step: int):
    stationary_because_unfree = set()
    proposed = {}
    for elf in elves:
        destination = propose_move_for(elf, elves, step)
        if destination == elf:
            stationary_because_unfree.add(elf)
        else:
            proposed[elf] = destination
    destination_freqs = Counter(proposed.values())
    stationary_because_bouncing = set()
    moving = set()
    for elf, destination in proposed.items():
        if destination_freqs[destination] > 1:
            stationary_because_bouncing.add(elf)
        else:
            moving.add(destination)
    return (
        stationary_because_unfree
        .union(stationary_because_bouncing)
        .union(moving))

def print_elves(elves: Elves) -> None:
    min_x = min(elves, key=lambda e: e.x).x
    max_x = max(elves, key=lambda e: e.x).x
    min_y = min(elves, key=lambda e: e.y).y
    max_y = max(elves, key=lambda e: e.y).y
    rows = []
    for y in range(max_y - min_y + 1):
      rows.append([])
      for x in range(max_x - min_x + 1):
          rows[-1].append('#' if Elf(x + min_x, y + min_y) in elves else '.')
    print('\n'.join(''.join(row) for row in rows))


  
    
def count_free_spaces(elves: Elves) -> int:
    min_x = min(elves, key=lambda e: e.x).x
    max_x = max(elves, key=lambda e: e.x).x
    
    min_y = min(elves, key=lambda e: e.y).y
    max_y = max(elves, key=lambda e: e.y).y
    area = (max_y - min_y + 1) * (max_x - min_x + 1)
    return area - len(elves)

def f(filename: str) -> int:
    elves = load(filename)
    for step in range(10):
        elves = move(elves, step)
    return count_free_spaces(elves)

def main():
    print(f('test_input.txt'))
    print(f('input.txt'))

if __name__ == '__main__':
    main()
