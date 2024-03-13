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

def matches(need: set[int], got: set[int]) -> int:
  "For part 1"
  matches = need.intersection(got)
  return len(matches)

def p1winnings(cards: Iterable[str]) -> int:
  total = 0
  for card in cards:
    n = matches(*parse_card(card)) 
    total += (2 ** (n - 1)) if n else 0
  return total


def mmul(cards: list[int], win: list[int]) -> list[int]:
  out = [0 for _ in cards]
  for i, (c, w) in enumerate(zip(cards, win)):
    for k in range(1, w + 1):
      out[i + k] += c
  return out


def p2winnings(cards: list[str]):
  win = [matches(*parse_card(card)) for card in cards]
  total = 0
  n = [1 for _ in win]
  while (to_add := sum(n)):
    total += to_add
    n = mmul(n, win)
  return total



def main():
  filenames = sys.argv[1:]
  for filename in filenames:
    cards = load(filename)
    print(p1winnings(cards))
    print(p2winnings(cards))
    print()



if __name__ == '__main__':
  main()
