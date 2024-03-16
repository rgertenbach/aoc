package.path = '/home/robin/lua/lib/?.lua;' .. package.path

local rstring = require "rstring"

local function parse_dims(s)
  local dims = {}
  for dim in rstring.split(s, 'x') do
    table.insert(dims, math.tointeger(dim))
  end
  table.sort(dims)
  return dims
end

local function required_area(dims)
  table.sort(dims)
  local extra = dims[1] * dims[2]
  return 3 * extra + 2 * dims[1] * dims[3] + 2 * dims[2] * dims[3]
end

local function load_input(filename)
  local f = assert(io.open(filename, "r"))
  local out = {}
  for row in f:lines() do
    table.insert(out, parse_dims(row))
  end
  return out
end

local function part1(filename)
  local boxes = load_input(filename)
  local total = 0
  for _, dims in pairs(boxes) do
    total = total + required_area(dims)
  end
  return total
end

local function ribbon_length(dims)
  table.sort(dims)
  return 2 * dims[1] + 2 * dims[2] + dims[1] * dims[2] * dims[3]
end

local function part2(filename)
  local boxes = load_input(filename)
  local total = 0
  for _, dims in pairs(boxes) do
    total = total + ribbon_length(dims)
  end
  return total

end


print(part1("input.txt"))
print(part2("input.txt"))
