package.path = "../utils/?.lua;" .. package.path
local su = require("string_utils")

local function parse_line(line)
  local cleaned = line:gsub(" +", " "):gsub("^ ", "")
  local a, b, c = table.unpack(su.split(cleaned, " "))
  return math.tointeger(a), math.tointeger(b), math.tointeger(c)
end

local function is_tri(a, b, c)
    return a + b > c and a + c > b and b + c > a
end

for i = 1, #arg do
  io.stdout:write(arg[i], "\n")
  local f = io.open(arg[i])
  if f == nil then
    io.stderr:write("Could not open ", arg[1])
    os.exit(1)
  end
  local possible = 0
  while true do
    local l1, l2, l3 = f:read("l"), f:read("l"), f:read("l")
    if l1 == nil then break end
    local a1, a2, a3 = parse_line(l1)
    local c1, c2, c3 = parse_line(l2)
    local b1, b2, b3 = parse_line(l3)
    if is_tri(a1, b1, c1) then possible = possible + 1 end
    if is_tri(a2, b2, c2) then possible = possible + 1 end
    if is_tri(a3, b3, c3) then possible = possible + 1 end
  end
  io.stdout:write(possible, "\n")
end
