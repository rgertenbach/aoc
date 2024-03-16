#!/usr/bin/python3

import re
import sys

def read_file(filename):
  with open(filename) as f:
    starts = f.readlines()

  return [int(start[-2]) for start in starts]

class Die:
  def __init__(self, sides):
    self.sides = sides
    self.last = sides
    self.total_rolls = 0

  def roll_once(self):
    if self.last == self.sides:
      self.last = 1
    else:
      self.last += 1
    self.total_rolls += 1
    return self.last

  def roll(self, n=3) -> int:
    total = 0
    for i in range(n):
      total += self.roll_once()
    return total

class Player:
  def __init__(self, pos, score=0):
    self.pos = pos
    self.score = score

  def move(self, die) -> None:
    steps = die.roll()
    self.pos += steps
    self.pos = (self.pos-1)%10+1
    self.score += self.pos

# ROll 3 times, add results
# move forward clockwise (1-10)
# icnrease value by the space they stopped on
# winer first to reach 1k

p1, p2 = read_file(sys.argv[1])
p1 = Player(p1)
p2 = Player(p2)
die = Die(100)

def play_until(thresh):
  while True:
    for p in [p1, p2]:
      p.move(die)
      if p.score >= 1000:
        return

play_until(1000)

print(min(p1.score, p2.score) * die.total_rolls)
