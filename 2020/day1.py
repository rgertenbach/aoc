#! /usr/bin/env python3
"""Finds the two entires that sum to 2020 and returns their product."""



with open('data/day1.txt') as f: numbers = f.readlines() 
numbers = sorted([int(number) for number in numbers])

for i in range(len(numbers) - 1):
  for j in range(i, len(numbers)):
    add = numbers[i] + numbers[j]
    if add == 2020:
      print(numbers[i] * numbers[j])
      exit()
    if add > 2020: 
      break

