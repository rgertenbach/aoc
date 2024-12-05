from collections import defaultdict

with open("input.txt") as f:
  manual = f.read().strip("\n")

rules, updates = manual.split("\n\n")
rules = [
    [int(x) for x in line.split("|")]
    for line in rules.split("\n")
]
updates = [
    [int(x) for x in update.split(",")]
    for update in updates.split("\n")
]


def make_deps(rules, update):
  s = set(update)
  deps = defaultdict(set)

  for dep, x in rules:
    if dep in s and x in s:
      deps[x].add(dep)
  return deps


def middle(pages):
  return pages[len(pages) // 2]

def is_correct(update, rules):
  done = set()
  deps = make_deps(rules, update)
  for x in update:

    if deps[x] - done: return False
    done.add(x)
  return True

def order(update, rules):
  deps = make_deps(rules, update)
  update = set(update)
  out = []
  done = set()
  while update:
    for x in update:
      if not deps[x] - done:
        out.append(x)
        done.add(x)
        update.remove(x)
        break
  return out



total = 0
for update in updates:
  if not is_correct(update, rules):
    fixed = order(update, rules)
    total += middle(fixed)

print(total)

