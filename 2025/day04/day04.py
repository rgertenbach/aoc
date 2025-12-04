import sys

with open(sys.argv[1]) as f:
    grid = [
        [x == "@" for x in line]
        for line in f.read().strip().split("\n")
    ]

rows = len(grid)
cols = len(grid[0])

def accessible(grid: list[list[bool]]) -> set[tuple[int, int]]:
    out = set()
    for row, line in enumerate(grid):
        for col, x in enumerate(line):
            if not x: continue
            neighbors = 0
            for pr in range(row - 1, row + 2):
                for pc in range(col - 1, col + 2):
                    if pr < 0: continue
                    if pc < 0: continue
                    if pr >= rows: continue
                    if pc >= cols: continue
                    if pr == row and pc == col: continue
                    neighbors += grid[pr][pc]
            if neighbors <= 3: out.add((row, col))
    return out


part1 = 0
part2 = 0

a = accessible(grid)
part1 = len(a)

while a:
    part2 += len(a)
    for r, c in a: grid[r][c] = False
    a = accessible(grid)

print(f"{part1 = }")
print(f"{part2 = }")
