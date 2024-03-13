import sys

def parse(s: str) -> list[int]: return [int(x) for x in s.split(' ')]
def diff(l: list[int]) -> list[int]: return [r - l for l, r in zip(l[:-1], l[1:])]


class Forecast:
  def __init__(self, series: list[int]):
    self.diffs = [series]
    while not all(x == 0 for x in self.diffs[-1]):
      self.diffs.append(diff(self.diffs[-1]))

  def one_step(self): return sum(diff[-1] for diff in self.diffs)


def part1(forecasts: list[Forecast]) -> int:
  return sum(forecast.one_step() for forecast in forecasts)


def main():
  for filename in sys.argv[1:]:
    with open(filename) as f: data = f.read().strip().split('\n')
    readings = [parse(row) for row in data]
    forecasts = [Forecast(reading) for reading in readings]
    print(part1(forecasts))

if __name__ == '__main__':
  main()
