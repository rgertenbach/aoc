from collections import namedtuple
import sys
sys.setrecursionlimit(10000)


Point = namedtuple('Point', ['x', 'y', 'z'])
Droplet = set[Point]
Box = tuple[Point, Point]

def load(filename: str) -> Droplet:
  with open(filename) as f:
    points = f.read().strip().split('\n')

  return set([Point(*[int(d) for d in point.split(',')]) for point in points])


def bounding_box(droplet: Droplet) -> Box:
  xmin = min(droplet, key=lambda p: p.x).x
  xmax = max(droplet, key=lambda p: p.x).x
  ymin = min(droplet, key=lambda p: p.y).y
  ymax = max(droplet, key=lambda p: p.y).y
  zmin = min(droplet, key=lambda p: p.z).z
  zmax = max(droplet, key=lambda p: p.z).z
  return Point(xmin, ymin, zmin), Point(xmax, ymax, zmax)


def neighbors(point: Point) -> list[Point]:
  return [
    Point(point.x + 1, point.y, point.z),
    Point(point.x - 1, point.y, point.z),
    Point(point.x, point.y + 1, point.z),
    Point(point.x, point.y - 1, point.z),
    Point(point.x, point.y, point.z + 1),
    Point(point.x, point.y, point.z - 1)]


def exposed_sides(point: Point, droplet: Droplet) -> int:
  exposed = 0
  for n in neighbors(point):
    if n not in droplet:
      exposed += 1
  return exposed


def externally_exposed_sides(point: Point, 
                             droplet: Droplet, 
                             space: dict) -> int:
  exposed = 0
  for n in neighbors(point):
    if n in droplet:
      continue
    if n in space and space[n]:
      exposed += 1

  return exposed


def far_outside_box(point: Point, box: Box) -> bool:
  return (
      point.x < box[0].x - 1 or point.x > box[1].x + 1
      or point.y < box[0].y - 1 or point.y > box[1].y + 1
      or point.z < box[0].z - 1 or point.z > box[1].z + 1)


def find_exposed_space(droplet: Droplet, box: Box) -> dict:
  space = {}
  frontier = [Point(box[0].x - 1, box[0].y - 1, box[0].z - 1)]
  while frontier:
    new_frontier = []
    for p in frontier:
      for n in neighbors(p):
        if n in space:
          continue
        elif n in droplet:
          space[n] = False
        elif far_outside_box(n, box ):
          continue
        else:
          space[n] = True
          new_frontier.append(n)
    frontier = new_frontier

  return space




def surface_area(droplet: Droplet) -> int:
  area = 0
  box = bounding_box(droplet)
  space = find_exposed_space(droplet, box)
  for point in droplet:
    # area += exposed_sides(point, droplet)
    area += externally_exposed_sides(point, droplet, space)
  return area


def main():
  test = surface_area(load('test_input.txt'))
  print(f'{test=}', 'Passed' if test == 58 else 'Failed!')
  # 2505 to smol
  print(surface_area(load('input.txt')))


if __name__ == '__main__':
  main()


# Find bounding box of droplet
# recursively check if non points are next to non points or a point but *not* 
# the bounding box. Use memoization
