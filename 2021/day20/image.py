LIT = '#'
LITF = '█'
OFF = '.'
OFFF = '·'

class Image:
  def __init__(self, vals, none_state=OFF):
    self.none_state = none_state
    self.vals = vals

  @classmethod
  def parse(cls, txt):
    lines = txt.strip().split('\n')
    return cls([list(line.strip()) for line in lines])

  def __getitem__(self, y, x):
    return self.vals[y][x]

  def __str__(self):
    def fline(line):
      return [(LITF if x == LIT else OFFF) for x in line]
    return '\n'.join([''.join(fline(line)) for line in self.vals])

  @property
  def height(self):
    return len(self.vals)

  @property
  def width(self):
    return len(self.vals[0])

  def pad(self):
    ns = self.none_state
    blank = [ns for _ in range(self.width + 2)]
    vals = [[ns] + row + [ns] for row in self.vals]
    return self.__class__([blank] + vals + [blank], ns)

  def __getitem__(self, tup):
    y, x = tup
    if y < 0 or y > self.height-1:
      return self.none_state
    if x < 0 or x > self.width-1:
      return self.none_state
    return self.vals[y][x]

  def enhanced_state(self, tup, algo):
    y, x = tup
    idx = 0
    for yy in [-1, 0, 1]:
      for xx in [-1, 0, 1]:
        idx = (idx << 1) + (self[y + yy, x + xx] == LIT)
    return algo[idx]

  def enhance(self, algo):
    padded = self.pad().pad()
    newvals = []
    for y in range(padded.height):
      newvals.append([])
      for x in range(padded.width):
        newvals[-1].append(padded.enhanced_state((y, x), algo))
    ns = algo[0 if self.none_state == OFF else -1]
    return self.__class__(newvals, ns)

  def n_lit(self):
    return sum(sum(x == LIT for x in line) for line in self.vals)



