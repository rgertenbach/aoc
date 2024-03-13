import sys
from enum import Enum
from collections import Counter

class HandType(Enum):
  HIGH = 1
  PAIR = 2
  TWOPAIR = 3
  THREE = 4
  FULL_HOUSE = 5
  FOUR = 6
  FIVE = 7

CARD_RANK = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14 }

class Hand:
  def __init__(self, cards: str):
    self.cards = cards
    self.hand_type = self.get_hand_type()

  def get_hand_type(self) -> HandType:
    c = Counter(self.cards)
    m = max(c.values())
    l = min(c.values())
    if m == 5: return HandType.FIVE
    if m == 4: return HandType.FOUR
    if m == 3 and l == 2: return HandType.FULL_HOUSE
    if m == 3: return HandType.THREE
    if len([f for f in c.values() if f == 2]) == 2: return HandType.TWOPAIR
    if m == 2: return HandType.PAIR
    return HandType.HIGH

  def __lt__(self, other: 'Hand') -> bool:
    if self.hand_type.value < other.hand_type.value: return True
    if self.hand_type.value > other.hand_type.value: return False
    for l, r in zip(self.cards, other.cards):
      if CARD_RANK[l] < CARD_RANK[r]: return True
      if CARD_RANK[l] > CARD_RANK[r]: return False
    return False

def part1(plays: list[tuple[Hand, int]]) -> int:
    plays = sorted(plays, key=lambda x: x[0])
    total = 0
    for i, (_, bid) in enumerate(plays):
      total += (i + 1) * bid
    return total

def main():
  for filename in sys.argv[1:]:
    with open(filename) as f:
      data = f.read().strip().split('\n')
    hand_bid_raw = [row.split(' ') for row in data]
    plays = [(Hand(hand), int(bid)) for hand, bid in hand_bid_raw]
    print(part1(plays))


if __name__ == '__main__':
  main()
