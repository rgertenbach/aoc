def is_monotonic(report: list[int]) -> bool:
  if report[1] > report[0]: return all(
      r > l for l, r in zip(report[:-1], report[1:])
  )
  return all(
      r < l for l, r in zip(report[:-1], report[1:])
  )

def is_safe(report: list[int]) -> bool:
  return is_monotonic(report) and all(
      abs(l - r) in [1, 2, 3]
      for l, r in zip(report[:-1], report[1:])
  )

def is_damped_safe(report: list[int]) -> bool:
  if is_safe(report): return True
  for i in range(len(report)):
    if is_safe(report[:i] + report[i+1:]): return True
  return False
with open("input.txt") as f:
    reports = [
        [int(level) for level in report.split(" ")]
        for report
        in f.read().strip("\n").split("\n")
    ]
    print(sum(is_damped_safe(report) for report in reports))
