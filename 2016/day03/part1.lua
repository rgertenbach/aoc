package.path = "../lua/?.lua;" .. package.path
local str = require("str")

for i = 1, #arg do
  io.stdout:write(arg[i], "\n")
  local f = io.open(arg[i])
  if f == nil then
    io.stderr:write("Could not open ", arg[1])
    os.exit(1)
  end
  local possible = 0
  for line in f:lines() do
    local a, b, c = table.unpack(str.split(line:gsub(" +", " "):gsub("^ ", ""), " "))
    a = math.tointeger(a)
    b = math.tointeger(b)
    c = math.tointeger(c)
    if a + b > c and a + c > b and b + c > a then possible = possible + 1 end
  end
  io.stdout:write(possible, "\n")
end
