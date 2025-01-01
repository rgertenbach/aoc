local f = assert(io.open("input.txt"))
RACE = 2503

local furthest = 0
for line in f:lines() do
  local deer, speed, dur, rest = line:match("^(%w+) can fly (%d+) .- (%d+) .- (%d+)")
  speed = tonumber(speed)
  dur = tonumber(dur)
  rest = tonumber(rest)

  local full_cycles, partial_cycle = RACE // (dur + rest), RACE % (dur + rest)
  local p1 = full_cycles * speed * dur + math.min(partial_cycle, dur) * speed
  if p1 > furthest then furthest = p1 end
end

print(furthest)
