local f = assert(io.open("input.txt"))
RACE = 2503

local reindeer = {}

for line in f:lines() do
  local name, speed, dur, rest = line:match("^(%w+) can fly (%d+) .- (%d+) .- (%d+)")
  speed = tonumber(speed)
  dur = tonumber(dur)
  rest = tonumber(rest)
  reindeer[name] = {speed = speed, dur = dur, rest = rest, points = 0, pos = 0}
end

for i = 0, RACE do
  local furthest = -1
  for _, stats in pairs(reindeer) do
    local is_moving = i % (stats.dur + stats.rest) < stats.dur
    if is_moving then stats.pos = stats.pos + stats.speed end
    if stats.pos > furthest then furthest = stats.pos end
  end
  for _, stats in pairs(reindeer) do
    if stats.pos == furthest then
      stats.points = stats.points + 1
    end
  end
end

local best = 0
for _, stats in pairs(reindeer) do
  if stats.points > best then best = stats.points end
end
print(best)
