#!/usr/local/bin/python3
import sys
from functools import cache
from collections import Counter, defaultdict


MAX_SCORE = 21


def read_file(filename):
  with open(filename) as f:
    starts = f.readlines()

  return [int(start[-2]) for start in starts]


@cache
def three_rolls(pos) -> dict:  # position: volume
  freqs = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
  return {(pos - 1 + mov) % 10 + 1: n for mov, n in freqs.items()}


def is_finished(state):
  return max(state[1], state[3]) >= MAX_SCORE


def all_states_finished(game):
  return all(is_finished(state) for state in game)


def next_round(games, whose_turn):
  isp1 = whose_turn == 1
  end_round = Counter()
  for state, n_init in games.items():
    if is_finished(state):
      end_round[state] += n_init
      continue
    p1pos, p1pts, p2pos, p2pts = state
    pos = p1pos if isp1 else p2pos
    outcomes = three_rolls(pos)
    for newpos, n in outcomes.items():
      newstate = (
        newpos if isp1 else p1pos,
        p1pts + (newpos if isp1 else 0),
        newpos if not isp1 else p2pos,
        p2pts + (newpos if not isp1 else 0))
      end_round[newstate] += n*n_init
  return end_round


def win_stats(games):
  p1wins = 0
  p2wins = 0
  for (_, p1pts, _, p2pts), n in games.items():
    if p1pts >= 21:
      p1wins += n
    else:
      p2wins += n
  return p1wins, p2wins


p1, p2 = read_file(sys.argv[1])
whose_turn = 1
game = {(p1, 0, p2, 0): 1}
while not all_states_finished(game):
  game = next_round(game, whose_turn)
  whose_turn = 2 if whose_turn == 1 else 1

p1wins, p2wins = win_stats(game)


print(f'p1: {p1wins}, p2: {p2wins}')
print(max(p1wins, p2wins))


