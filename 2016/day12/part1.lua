local f = assert(io.open("input.txt"))
local json = f:read("*l")

local total = 0
for number in json:gmatch("(%-?%d+)") do
  total = total + tonumber(number)
end
print(total)
