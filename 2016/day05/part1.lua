package.path = "../utils/?.lua;" .. package.path
local md5 = require("md5")

--- @param door_id string
local function findpw(door_id)
  local pw = ""
  local sum
  local hex
  local i = 0
  while #pw < 8 do
    repeat
      i = i + 1
      local input = string.format("%s%i", door_id, i)
      sum = md5.sum(input)
      hex = md5.tohex(sum)
    until hex:sub(1, 5) == "00000"

    io.stdout:write(string.format("%s: %s\n", sum, hex))
    pw = pw .. hex:sub(6, 6)
  end
  return pw
end


while true do
  io.stdout:write("Door ID: ")
  local door = io.stdin:read("*l")
  if door == "" then break end
  print(findpw(door))

end
