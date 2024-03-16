def one_contains_other(assignment) -> bool:
  elf1, elf2 = assignment.strip().split(',')
  elf1 = [int(part) for part in elf1.split('-')]
  elf2 = [int(part) for part in elf2.split('-')]
  return ((elf1[0] <= elf2[0] and elf1[1] >= elf2[1]) or
          (elf1[0] >= elf2[0] and elf1[1] <= elf2[1]) or

          (elf2[0] <= elf1[0] <= elf2[1]) or
          (elf1[0] <= elf2[0] <= elf1[1]) or
          (elf2[0] <= elf1[1] <= elf2[1]) or
          (elf1[0] <= elf2[1] <= elf1[1]))


with open('input.txt') as f:
  assignments = f.readlines()

print(sum(one_contains_other(ass) for ass in assignments))



