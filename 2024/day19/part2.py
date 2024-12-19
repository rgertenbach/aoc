from functools import cache
with open("input.txt") as f:
  colors, patterns = f.read().strip("\n").split("\n\n")
  colors = colors.split(", ")
  patterns = patterns.split("\n")

@cache
def possible(pattern: str) -> int:
  if pattern == "": return True
  return sum((possible(pattern.removeprefix(c)) for c in colors if pattern.startswith(c)))

print(sum(possible(p) for p in patterns))



