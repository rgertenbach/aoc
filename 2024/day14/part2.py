import re
filename = "input.txt"
HEIGHT = 103 if filename == "input.txt" else 7
WIDTH = 101 if filename == "input.txt" else 11

def parse_robot(line: str):
  [(x, y, vx, vy)] = re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
  return int(x), int(y), int(vx), int(vy)

with open("input.txt") as f:
  robots = [parse_robot(line) for line in f.read().strip("\n").split("\n")]

def simulate(robot, n: int) -> tuple[int, int, int, int]:
  x, y, vx, vy = robot
  x = (x + vx * n) % WIDTH
  y = (y + vy * n) % HEIGHT
  return x, y, vx, vy

def plot(robots: list[tuple[int, int, int, int]]) -> str:
  out = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
  for x, y, _, _ in robots: out[y][x] = "O"
  return "\n".join(("".join(line) for line in out))


i = 0

while True:
  robots = [simulate(robot, 1) for robot in robots]
  if 'OOOOOOOO' in plot(robots):
    print(plot(robots))
    print(i)
    input()

  i += 1
