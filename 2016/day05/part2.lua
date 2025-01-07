package.path = "../lua/?.lua;" .. package.path
local md5 = require("md5")

local function has_all(t, n)
  for i = 1, n do
    if t[i] == nil then return false end
  end
  return true
end

--- @param door_id string
local function findpw(door_id)
  local pw = {}
  local sum
  local hex
  local i = 0
  while not has_all(pw, 8) do
    repeat
      i = i + 1
      local input = string.format("%s%i", door_id, i)
      sum = md5.sum(input)
      hex = md5.tohex(sum)
    until hex:sub(1, 5) == "00000"
    io.stdout:write(string.format("%s: %s\n", sum, hex))
    local pos_raw = hex:sub(6, 6)
    if pos_raw:match("%d") then
      local pos = math.tointeger(pos_raw) + 1
      if pw[pos] == nil then
        pw[pos] = hex:sub(7, 7)
      end
    end
  end
  return table.concat(pw, ""):sub(1, 8)
end


while true do
  io.stdout:write("Door ID: ")
  local door = io.stdin:read("*l")
  if door == "" then break end
  print(findpw(door))

end
