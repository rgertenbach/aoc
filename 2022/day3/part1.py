from collections import Counter


class Rucksack:
  def __init__(self, s):
    s = s.strip()
    self.left = s[:int(len(s) / 2)]
    self.right = s[int(len(s) / 2):]

  def find_double(self):
    l = Counter(self.left)
    r = Counter(self.right)
    dupe = l & r
    return dupe.most_common(1)[0][0]


def priority(letter):
  if letter.islower():
    return ord(letter) - ord('a') + 1

  return ord(letter) - ord('A') + 27



with open('input.txt') as f:
  rucksacks = f.readlines()

print(sum(priority(Rucksack(rucksack).find_double()) for rucksack in rucksacks))
  



