from typing import NamedTuple

class Block(NamedTuple):
  position: int
  next: int
  id: int

  @property
  def size(self) -> int: return self.next - self.position

  @property
  def checksum(self):
    return sum(p * self.id for p in range(self.position, self.next))


with open("input.txt") as f:
  file = f.read().strip("\n")

drive = []
is_file = True
current_id = 0
position = 0
for s in file:
  if is_file: drive.append(Block(position, position + int(s), current_id))
  current_id += is_file
  is_file = not is_file
  position += int(s)

while current_id > 0:
  current_id -= 1
  # Find current
  current_i = 0
  while current_i < len(drive):
    if drive[current_i].id == current_id: break
    current_i += 1
  if current_i >= len(drive): raise RuntimeError(f"no current {current_id} found")
  current = drive[current_i]

  # Move current if possible
  for after_i in range(len(drive) - 1):
    if after_i >= current_i: break
    if drive[after_i + 1].position - drive[after_i].next >= current.size:
      drive = (
          drive[:after_i + 1]
          + [Block(drive[after_i].next, drive[after_i].next + current.size, current.id)]
          + drive[after_i + 1:current_i]
          + drive[current_i+1:]
      )
      break

print(sum(f.checksum for f in drive))
