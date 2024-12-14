import re
filename = "input.txt"
HEIGHT = 103 if filename == "input.txt" else 7
WIDTH = 101 if filename == "input.txt" else 11

def parse_robot(line: str):
  [(x, y, vx, vy)] = re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
  return int(x), int(y), int(vx), int(vy)

with open("input.txt") as f:
  robots = [parse_robot(line) for line in f.read().strip("\n").split("\n")]

def simulate(robot, n: int) -> tuple[int, int]:
  x, y, vx, vy = robot
  x = (x + vx * n) % WIDTH
  y = (y + vy * n) % HEIGHT
  return x, y

q1, q2, q3, q4 = 0, 0, 0, 0
for robot in robots:
  x, y = simulate(robot, 100)
  if x < WIDTH // 2 and y < HEIGHT // 2: q1 += 1
  if x > WIDTH // 2 and y < HEIGHT // 2: q2 += 1
  if x < WIDTH // 2 and y > HEIGHT // 2: q3 += 1
  if x > WIDTH // 2 and y > HEIGHT // 2: q4 += 1
print(q1 * q2 * q3 * q4)
