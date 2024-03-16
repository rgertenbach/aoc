import sys
import z3

# https://github.com/DarthGandalf/advent-of-code/blob/master/2023/day24p2.py
V3 = list[int]

def parse_vector(s: str) -> V3:
  return list(int(p) for p in s.split(', '))

def parse_rock(s: str) -> tuple[V3, V3]:
  left, right = s.split(' @ ')
  return parse_vector(left), parse_vector(right)

def part2(stones: list[tuple[V3, V3]]) -> int:
  s = z3.Solver()
  # params of the rock we throw
  px, py, pz, vx, vy, vz = z3.Ints('px py pz vx vy vz')
  for i, (pos, vec) in enumerate(stones):
    t = z3.Int(f't{i}')
    pxi, pyi, pzi = z3.Ints(f'px{i} py{i} pz{i}')
    vxi, vyi, vzi = z3.Ints(f'vx{i} vy{i} vz{i}')

    s.add(pxi == pos[0])
    s.add(pyi == pos[1])
    s.add(pzi == pos[2])
    s.add(vxi == vec[0])
    s.add(vyi == vec[1])
    s.add(vzi == vec[2])

    s.add(t >= 0)  # time of collision must not be in the past
    s.add(pxi + t * vxi == px + t * vx)
    s.add(pyi + t * vyi == py + t * vy)
    s.add(pzi + t * vzi == pz + t * vz)
  r = s.check()
  print(f'checked {r}')
  m = s.model()
  #print(m)
  return int(str(m[px])) + int(str(m[py])) + int(str(m[pz]))




def main() -> None:
  for filename in sys.argv[1:]:
    print(filename)
    with open(filename) as f:
      data = f.read().strip().split('\n')
    stones = [parse_rock(s) for s in data]
    print(part2(stones[:5]))


if __name__ == '__main__':
  main()
