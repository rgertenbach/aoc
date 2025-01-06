package.path = "../lua/?.lua;" .. package.path
local str = require("str")
local tbl = require("tbl")

local KEYPAD = {
  {1, 2, 3},
  {4, 5, 6},
  {7, 8, 9}
}

local function part1(instructions)
  local x, y = 2, 2  -- 5
  local out = 0
  for instruction in tbl.valuesi(instructions) do
    local moves = str.split(instruction, "")
    for move in tbl.valuesi(moves) do
      if move == "U" and y > 1 then y = y - 1
      elseif move == "D" and y < 3 then y = y + 1
      elseif move == "L" and x > 1 then x = x - 1
      elseif move == "R" and x < 3 then x = x + 1
      end
    end
    out = out * 10
    out = out + KEYPAD[y][x]
  end
  return out
end

local function main()
  for i = 1, #arg do
    local filename = arg[i]
    io.stdout:write(filename, "\n")
    local file = io.open(filename, "r")
    if file == nil then
      io.stderr:write(string.format("Could not open %s\n", filename))
      os.exit(1)
    end
    local instructions_raw = file:read("a")
    file:close()
    local instructions = str.split(instructions_raw, "\n")
    io.stdout:write(part1(instructions), "\n")
  end
end

main()
