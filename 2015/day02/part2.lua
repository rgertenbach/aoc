local function ribbon(dims)
  table.sort(dims)
  return 2 * dims[1] + 2 * dims[2] + dims[1] * dims[2] * dims[3]
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
  total = total + ribbon(parse_dims(line))
end
print(total)
