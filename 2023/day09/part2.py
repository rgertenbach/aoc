import sys

def parse(s: str) -> list[int]: return [int(x) for x in s.split(' ')]
def diff(l: list[int]) -> list[int]: return [r - l for l, r in zip(l[:-1], l[1:])]


class Forecast:
  def __init__(self, series: list[int]):
    self.diffs = [series]
    while not all(x == 0 for x in self.diffs[-1]):
      self.diffs.append(diff(self.diffs[-1]))

  def forward(self): return sum(diff[-1] for diff in self.diffs)
  def backward(self):
    prev = 0
    for diff in self.diffs[::-1]: prev = diff[0] - prev
    return prev


def main():
  for filename in sys.argv[1:]:
    with open(filename) as f: data = f.read().strip().split('\n')
    readings = [parse(row) for row in data]
    forecasts = [Forecast(reading) for reading in readings]
    print(sum(forecast.forward() for forecast in forecasts))
    print(sum(forecast.backward() for forecast in forecasts))
    print()

if __name__ == '__main__':
  main()
