import sys
from typing import NamedTuple

def load(filename: str) -> list[str]:
  with open(filename) as f: return f.readlines()

class Draw(NamedTuple):
  red: int = 0
  green: int = 0
  blue: int = 0

  @classmethod
  def parse_draw(cls, draw: str):
    cubes = draw.strip(' ').split(', ')
    r, g, b = 0, 0, 0
    for cube in cubes:
      n, color = cube.split(' ')
      if color == 'red': r = int(n)
      elif color == 'green': g = int(n)
      else: b = int(n)
    return cls(r, g, b)

  @property
  def power(self):
    return self.red * self.green * self.blue

def parse_game(game: str):
  game_id, outcomes = game.split(':')
  outcomes = outcomes.strip('\n')
  game_id = game_id.lstrip('Game ')
  rounds = outcomes.split(';')
  return int(game_id), [Draw.parse_draw(round) for round in rounds]

def is_possible(draws: list[Draw]) -> bool:
  max_red = 12
  max_green = 13
  max_blue = 14
  for draw in draws:
    if draw.red > max_red: return False
    if draw.green > max_green: return False
    if draw.blue > max_blue: return False
  return True

def min_cubes(draws: list[Draw]) -> Draw:
  max_red = max(draws, key=lambda draw: draw.red).red
  max_green = max(draws, key=lambda draw: draw.green).green
  max_blue = max(draws, key=lambda draw: draw.blue).blue
  return Draw(max_red, max_green, max_blue)


def main():
  filename = sys.argv[1]
  games = load(filename)
  possible = 0
  powers = 0
  for game in games:
    game_id, draws = parse_game(game)
    if (is_possible(draws)): possible += game_id # part 1
    powers += min_cubes(draws).power

  print(possible)
  print(powers)

if __name__ == "__main__":
  main()
