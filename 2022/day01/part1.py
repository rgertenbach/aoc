with open('input.txt') as f:
  cals = f.readlines()

highest = 0
current = 0

for cal in cals:
  cal = cal.strip()
  if cal == '':
    highest = max(highest, current)
    current = 0
    continue
  current += int(cal.strip('\n'))

print(highest)
  


