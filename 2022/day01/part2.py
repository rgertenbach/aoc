with open('input.txt') as f:
  cals = f.readlines()

highest = 0
current = 0
elves = []

for cal in cals:
  cal = cal.strip()
  if cal == '':
    elves.append(current)
    current = 0
    continue
  current += int(cal.strip('\n'))
elves.append(current)

print(sum(sorted(elves)[-3:]))
  


