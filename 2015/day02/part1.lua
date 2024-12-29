local function surface(length, width, height)
  local a1 = length * width
  local a2 = width * height
  local a3 = length * height
  return 2 * a1 + 2 * a2 + 2 * a3 + math.min(a1, a2, a3)
end

local function parse_dims(line)
  local dims = {}
  for dim in line:gmatch("%d+") do
    table.insert(dims, tonumber(dim))
  end
  return dims
end

local f = assert(io.open("input.txt"))
local total = 0
for line in f:lines() do
  local dims = parse_dims(line)
  total = total + surface(table.unpack(dims))
end
print(total)
