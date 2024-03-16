from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z'])
Droplet = set[Point]

def load(filename: str) -> Droplet:
  with open(filename) as f:
    points = f.read().strip().split('\n')

  return set([Point(*[int(d) for d in point.split(',')]) for point in points])


def exposed_sides(point: Point, droplet: Droplet) -> int:
  exposed = 0

  if Point(point.x + 1, point.y, point.z) not in droplet:
    exposed += 1
  if Point(point.x - 1, point.y, point.z) not in droplet:
    exposed += 1

  if Point(point.x, point.y + 1, point.z) not in droplet:
    exposed += 1
  if Point(point.x, point.y - 1, point.z) not in droplet:
    exposed += 1

  if Point(point.x, point.y, point.z + 1) not in droplet:
    exposed += 1
  if Point(point.x, point.y, point.z - 1) not in droplet:
    exposed += 1

  return exposed


def surface_area(droplet: Droplet) -> int:
  area = 0
  for point in droplet:
    area += exposed_sides(point, droplet)
  return area


def main():
  print(surface_area(load('smol.txt')))
  print(surface_area(load('test_input.txt')))
  print(surface_area(load('input.txt')))


if __name__ == '__main__':
  main()


