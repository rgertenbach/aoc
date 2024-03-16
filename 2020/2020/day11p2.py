#!/usr/bin/env python3


with open('data/day11.txt') as f:
  seats = f.readlines()

seats = [list(row.strip('\n')) for row in seats]


def update(seats):
  rows = len(seats)
  cols = len(seats[0])
  new = []
  for row in range(rows):
    newrow = []
    for col in range(cols):
      adjacent = 0
      # Top left
      if row > 0 and col > 0 and seats[row-1][col-1] == '#':
        adjacent += 1
      # Top 
      if row > 0 and seats[row-1][col] == '#':
        adjacent += 1
      # Top Right
      if row > 0 and col < cols-1 and seats[row-1][col+1] == '#':
        adjacent += 1
      # Left
      if col > 0 and seats[row][col-1] == '#':
        adjacent += 1
      # Right
      if col < cols-1 and seats[row][col+1] == '#':
        adjacent += 1
      # Bottom left
      if row < rows-1 and col > 0 and seats[row+1][col-1] == '#':
        adjacent += 1
      # Bottom 
      if row < rows-1 and seats[row+1][col] == '#':
        adjacent += 1
      # Bottom Right
      if row < rows-1 and col < cols-1 and seats[row+1][col+1] == '#':
        adjacent += 1

      if seats[row][col] == '.':
        newrow.append('.')
      elif adjacent == 0:
        newrow.append('#')
      elif seats[row][col] == '#' and adjacent >= 4:
        newrow.append('L')
      else:
          newrow.append(seats[row][col])
    new.append(newrow)
  return new

def same(a, b):
  for rowa, rowb in zip(a, b):
    for cola, colb in zip(rowa, rowb):
      if cola != colb:
        return False
  return True

def update_until_static(seats):
  new = update(seats)
  if same(seats, new):
    return seats
  else:
    return update_until_static(new)

final = update_until_static(seats)


for row in final:
  print(''.join(row))
print(sum(x == '#' for row in final for x in row))
