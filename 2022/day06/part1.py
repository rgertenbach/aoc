import re
from collections import Counter

def is_start_of_packet(x):
  c = Counter(x)
  return c.most_common(1)[0][1] == 1


with open('input.txt') as f:
  buf = f.read().strip('\n')


for i in range(len(buf) - 3):
  if is_start_of_packet(buf[i:i+4]):
    print(i+4)
    break
