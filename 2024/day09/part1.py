from typing import NamedTuple

EMPTY = '.'

with open("input.txt") as f:
  file = f.read().strip("\n")

drive = []
is_file = True
current_id = 0
for s in file:
  drive.extend([(current_id if is_file else EMPTY)] * int(s))
  current_id += is_file
  is_file = not is_file


left = 0
right = len(drive) - 1
while left < right:
  if drive[left] != EMPTY:
    left += 1
    continue
  if drive[right] == EMPTY:
    right -= 1
    continue
  drive[left], drive[right] = drive[right], EMPTY

def checksum(drive):
  s = 0
  for i, file_id in enumerate(drive):
    if file_id == EMPTY: break
    s += i * file_id
  return s
print(drive)
print(checksum(drive))
      

