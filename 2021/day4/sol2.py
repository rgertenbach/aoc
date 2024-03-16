#!/usr/bin/python3
import re
import sys

def parse_board(board):
  def parse_row(row):
    return re.split(' +', row)

  return [parse_row(row.strip()) for row in board]

def load(filename):
  with open(filename) as f:
    lines = f.readlines()
  draws = lines[0].strip().split(',')
  allboards = lines[2:]
  splitboards = []
  current_board = []
  
  # Parse boards
  for row in allboards:
    if row == '\n':
      splitboards.append(current_board)
      current_board = []
    else:
      current_board.append(row)
  else:
    splitboards.append(current_board)

  splitboards = [parse_board(board) for board in splitboards]

  return draws, splitboards

class Board:
  def __init__(self, board):
    self.board = board
    self.matches = []
    self.size = 5  # Constant


  def check_draw(self, draw):
    for rowi, row in enumerate(self.board):
      for coli, col in enumerate(row):
        if col == draw:
          match = (rowi, coli)
          self.matches.append((match))
          return match

  def check_win(self):
    rows = [0 for _ in range(self.size)]
    cols = [0 for _ in range(self.size)]
    for rowi, coli in self.matches:
      rows[rowi] += 1
      cols[coli] += 1

    return  5 in rows or 5 in cols

  def value(self):
    total = 0
    for rowi, row in enumerate(self.board):
      for coli, col in enumerate(row):
        if (rowi, coli) not in self.matches:
          total += int(col)
    return total

def bingo(draws, boards):
  for draw in draws:
    for board in boards:
      board.check_draw(draw)
      if len(boards) == 1 and board.check_win():
        return int(board.value()) * int(draw)
    boards = [board for board in boards if not board.check_win()]

  

if __name__ == '__main__':
  draws, boards = load(sys.argv[1])
  boards = [Board(board) for board in boards]
  winner = bingo(draws, boards)
  print(winner)

