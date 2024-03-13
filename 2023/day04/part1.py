import re
import sys
from typing import Iterable

def load(filename: str) -> list[str]:
  with open(filename) as f:
    return f.read().strip('\n').split('\n')

def parse_numbers(s: str) -> list[int]:
  f = re.sub(' +', ' ', s.strip()).split(' ')
  return [int(x) for x in f]

def parse_card(card: str) -> tuple[set[int], set[int]]:
  card = re.sub(r'Card +\d+: ', '', card)
  need, got = card.split(' | ')
  return set(parse_numbers(need)), set(parse_numbers(got))

def points(need: set[str], got: set[str]) -> int:
  matches = need.intersection(got)
  if matches: return 2 ** (len(matches) - 1)
  return 0

def winnings(cards: Iterable[str]) -> int:
  total = 0
  for card in cards:
    total += points(*parse_card(card))
  return total


def main():
  filenames = sys.argv[1:]
  for filename in filenames:
    cards = load(filename)
    print(winnings(cards))


if __name__ == '__main__':
  main()
