import random

def parse_input(line: str) -> tuple[str, int]:
  name, val = line.split(": ")
  return name, int(val)

def parse_gate(line: str) -> tuple[str, tuple[str, str, str]]:
  inputs, output = line.split(" -> ")
  a, op, b = inputs.split(" ")
  return output, (a, op, b)


def evaluate_circuit(gates: dict[str, tuple[str, str, str]], x: int, y: int) -> dict[str, bool]:
  xs = [int(digit) for digit in f"{x:045b}"][::-1]
  ys = [int(digit) for digit in f"{y:045b}"][::-1]
  should = f"{x + y:046b}"[::-1]
  state = {}
  zs = [z for z in gates.keys() if z.startswith("z")]
  def evaluate(node: str) -> int:
    if node.startswith("x"): return xs[int(node.removeprefix("x"))]
    if node.startswith("y"): return ys[int(node.removeprefix("y"))]
    if node in state: return state[node]
    a, op, b = gates[node]
    if op == "AND": return evaluate(a) & evaluate(b)
    if op == "OR": return evaluate(a) | evaluate(b)
    if op == "XOR": return evaluate(a) ^ evaluate(b)
    raise RuntimeError("fallthrough")
  return {z: evaluate(z) == int(should[int(z.removeprefix("z"))]) for z in zs}


with open("input.txt") as f:
  inputs, gates = f.read().strip("\n").split("\n\n")
  inputs = [parse_input(input) for input in inputs.split("\n")]
  gates = dict(parse_gate(gate) for gate in gates.split("\n"))

state = {z: True for z in gates.keys() if z.startswith("z")}

swaps = [
    ("gvw", "qjb"),
    ("z15", "jgc"),
    ("drg", "z22"),
    ("z35", "jbp"),
]
for t1, t2 in swaps:
  gates[t1], gates[t2] = gates[t2], gates[t1]

for _ in range(200):
  x = random.randint(0, 1 << 45)
  y = random.randint(0, 1 << 45)
  for z, correct in evaluate_circuit(gates, x, y).items():
    state[z] = state[z] and correct

with open("output.txt", "w") as f:
  f.write("digraph G {\n")
  f.write("node [style=filled]\n")
  for i in range(45):
      f.write(f"x{i:02} [color=yellow]\n")
      f.write(f"y{i:02} [color=yellow]\n")
      z = f"z{i:02}"
      f.write(f"{z} [color={'green' if state[z] else 'red'}]\n")
  f.write(f"z45 [color={'green' if state['z45'] else 'red'}]\n")
  for out, (a, op, b) in gates.items():
        f.write(f"{a} -> {out}  [label={op}]\n")
        f.write(f"{b} -> {out}  [label={op}]\n")
  f.write("}\n")

wires = []
for a, b in swaps:
  wires.append(a)
  wires.append(b)

print(",".join(sorted(wires)))
