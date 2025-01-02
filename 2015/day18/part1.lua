ON = "#"
OFF = "."
local f = assert(io.open("input.txt"))

local lights = {}
for line in f:lines() do
  table.insert(lights, {})
  for i = 1, #line do
    table.insert(lights[#lights], line:sub(i, i))
  end
end
f:close()

local function neighbors_on(lights, r, c)
  local on = 0
  if r > 1 and c > 1 and lights[r-1][c-1] == ON then on = on + 1 end
  if r > 1 and lights[r-1][c] == ON then on = on + 1 end
  if r > 1 and c < #lights and lights[r-1][c+1] == ON then on = on + 1 end
  if c > 1 and lights[r][c-1] == ON then on = on + 1 end
  if c < #lights and lights[r][c+1] == ON then on = on + 1 end
  if r < #lights and c > 1 and lights[r+1][c-1] == ON then on = on + 1 end
  if r < #lights and lights[r+1][c] == ON then on = on + 1 end
  if r < #lights and c < #lights and lights[r+1][c+1] == ON then on = on + 1 end
  return on
end

local function step(lights)
  local new = {}
  for row, line in ipairs(lights) do
    table.insert(new, {})
    for col, x in ipairs(line) do
      local n = neighbors_on(lights, row, col)
      if x == ON then
        if n == 2 or n == 3 then table.insert(new[#new], ON) else table.insert(new[#new], OFF) end
      else
        if n == 3 then table.insert(new[#new], ON) else table.insert(new[#new], OFF) end
      end
    end
  end
  return new
end

local function printlights(lights)
  local lines = {}
  for _, line in ipairs(lights) do
    table.insert(lines, table.concat(line))
  end
  return table.concat(lines, "\n")
end

local function lightson(lights)
  local on = 0
  for _, line in ipairs(lights) do
    for _, x in ipairs(line) do
      if x == ON then on = on + 1 end
    end
  end
  return on
end

for _ = 1, 100 do
  lights = step(lights)
end
print(lightson(lights))
