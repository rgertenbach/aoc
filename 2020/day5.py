#!/usr/bin/env python3

def parse_seat(seat):
  row = seat[:7]
  row = int(''.join('1' if x == 'B' else '0' for x in row), 2)
  col = seat[7:]
  col = int(''.join('1' if x == 'R' else '0' for x in col), 2)
  return row * 8 + col

with open('data/day5.txt') as f:
  tickets = f.readlines()

print(max(parse_seat(ticket.strip()) for ticket in tickets))
