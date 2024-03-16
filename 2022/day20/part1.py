class CLE:
  def __init__(self, value, left=None, right=None):
    self.val = value
    self.left = left
    self.right = right
    self.l = None

  def move_right(self, n: int) -> None:
    n %= (len(self) - 1)
    if n == 0:
      return
    newl = self[n]
    newr = newl.right
    oldl = self.left
    oldr = self.right

    oldl.right = oldr
    oldr.left = oldl
    self.left = newl
    self.right = newr
    newl.right = self
    newr.left = self

  def move(self) -> None:
    if self.val == 0:
      return
    if self.val > 0:
      self.move_right(self.val)
    else:
      self.move_left(abs(self.val))

  def move_left(self, n: int) -> None:
    n %= (len(self) - 1)
    if n == 0:
      return

    newr = self[len(self) - n]
    if newr.left == self:
      return

    newl = newr.left
    oldl = self.left
    oldr = self.right
    oldl.right = oldr
    oldr.left = oldl

    self.left = newl
    self.right = newr

    newr.left = self
    newl.right = self

  def __len__(self) -> int:
    return self.l

  def __getitem__(self, n) -> 'CLE':
    n = n % len(self)
    goal = self
    for i in range(n):
      goal = goal.right
    return goal

  def find(self, val) -> 'CLE':
    x = self
    i = 0
    visited = set()
    while x.val != val:
      if x in visited:
        raise RuntimeError(f'Found a loop at {x.val}')
      visited.add(x)
      x = x.right
      i = i + 1

      if x == self:
        raise RuntimeError(f'No {val} found')
    return x

  def __str__(self) -> str:
    out = []
    out.append(self.val)
    x = self
    while (x := x.right) != self:
      out.append(x.val)
    return str(out)
    

def load(filename: str) -> list[CLE]:
  with open(filename) as f:
    nodes = f.read().strip().split('\n')
  out = []
  for n in nodes:
    val = int(n)
    node = CLE(val)
    node.l = len(nodes)
    if out:
      node.left = out[-1]
      out[-1].right = node
    out.append(node)

  out[0].left = out[-1]
  out[-1].right = out[0]

  return out


def process(l: list[CLE]) -> CLE:
  # print('Initial state:\n', l[0])
  for i, e in enumerate(l):
    e.move()
    # print(l[0])
  return l[0]



def main():
  l = load('input.txt')
  print('Processing')
  process(l)

  head = l[0].find(0)
  total = 0

  head = head[1000]
  total += head.val

  head = head[1000]
  total += head.val

  head = head[1000]
  total += head.val
  print(total, 'PASSED' if total == 16533 else 'FAILED')



if __name__ == '__main__':
  main()


# not 8701 is too low
