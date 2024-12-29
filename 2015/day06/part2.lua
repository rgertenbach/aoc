-- Justification for being lazy?
local lights = {}
for row = 1,1000 do
  table.insert(lights, {})
  for _ = 1, 1000 do
    table.insert(lights[row], 0)
  end
end

---@param line string
local function parse_line(line)
  local action, sr,sc, er,ec = line:match("(%D+)(%d+),(%d+) through (%d+),(%d+)")
  return action, tonumber(sr), tonumber(sc), tonumber(er), tonumber(ec)
end

local f = assert(io.open("input.txt"))
for line in f:lines() do
  local action, sr, sc, er, ec = parse_line(line)
  for row = sr+1,er+1 do
    for col = sc+1,ec+1 do
      if action == "turn on " then
        lights[row][col] = lights[row][col] + 1
      elseif action == "turn off " then
        lights[row][col] = math.max(lights[row][col] - 1, 0)
      elseif action == "toggle " then
        lights[row][col] = lights[row][col] + 2
      end
    end
  end
end
local total = 0
for row = 1,1000 do
  for col = 1, 1000 do
    total = total + lights[row][col]
  end
end
print(total)
