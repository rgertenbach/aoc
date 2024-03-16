from collections import Counter

def is_start_of_packet(x):
  c = Counter(x)
  return c.most_common(1)[0][1] == 1


with open('input.txt') as f:
  buf = f.read().strip('\n')


for i in range(len(buf) - 13):
  if is_start_of_packet(buf[i:i+14]):
    print(i+14)
    break
