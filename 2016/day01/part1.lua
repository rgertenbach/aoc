package.path = "../utils/?.lua;" .. package.path
local su = require("string_utils")

local function parse(s)
  local out = {}
  out.dir = s:sub(1, 1)
  out.amt = math.tointeger(s:sub(2, #s))
  return out
end

local FACE = {
  UR = "R", UL = "L",
  DR = "L", DL = "R",
  RR = "D", RL = "U",
  LR = "U", LL = "D",
}


local function main()
  for i = 1, #arg do
    print(arg[i])
    local file = io.open(arg[i], "r")
    if file == nil then
      print("Could not open " .. arg[i])
      os.exit(1)
    end
    local data = file:read("a")
    file:close()
    local moves = su.split(data, ", ")
    local pos = {x = 0, y = 0, f="U"}
    for _, move in ipairs(moves) do
      local m = parse(move)
      pos.f = FACE[pos.f .. m.dir]
      if pos.f == "L" then pos.x = pos.x - m.amt
      elseif pos.f == "R" then pos.x = pos.x + m.amt
      elseif pos.f == "U" then pos.y = pos.y - m.amt
      elseif pos.f == "D" then pos.y = pos.y + m.amt
      else print("Panic") os.exit(1)
      end
    end
    print(math.abs(pos.x) + math.abs(pos.y))

  end
end

main()
