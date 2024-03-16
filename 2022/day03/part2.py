from collections import Counter


def priority(letter):
  if letter.islower():
    return ord(letter) - ord('a') + 1

  return ord(letter) - ord('A') + 27

with open('input.txt') as f:
  rucksacks = f.readlines()

rucksacks = [Counter(rucksack.strip()) for rucksack in rucksacks]


n = len(rucksacks)
n_sets = int(n / 3)

points = 0

for i in range(n_sets):
  group = rucksacks[3 * i:3 * i + 3]
  
  intersection = group[0] & group[1]
  intersection &= group[2]
  points += priority(intersection.most_common(1)[0][0])


print(points)



