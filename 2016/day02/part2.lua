package.path = "../lua/?.lua;" .. package.path
local str = require("str")
local tbl = require("tbl")

local KEYPAD = {
  {1, 2, 3},
  {4, 5, 6},
  {7, 8, 9}
}

local KEYPAD2 = {
  {nil, nil, 1},
  {nil , 2, 3, 4},
  {5, 6, 7, 8, 9},
  {nil, "A", "B", "C"},
  {nil, nil, "D"}
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

local function part2(instructions)
  local x, y = 1, 3  -- 5
  local out = ""
  for instruction in tbl.valuesi(instructions) do
    local moves = str.split(instruction, "")
    for move in tbl.valuesi(moves) do
      if move == "U" then
        if y == 2 and x == 3 then y = y - 1
        elseif (y == 3 or y == 4) and (x == 2 or x == 3 or x == 4) then y = y - 1
        elseif y == 5 and x == 3 then y = y - 1
        end
      elseif move == "D" then
        if y == 4 and x == 3 then y = y + 1
        elseif (y == 2 or y == 3) and (x == 2 or x == 3 or x == 4) then y = y + 1
        elseif y == 1 and x == 3 then y = y + 1
        end
      elseif move == "L" then
        if x == 2 and y == 3 then x = x - 1
        elseif (x == 3 or x == 4) and (y == 2 or y == 3 or y == 4) then x = x - 1
        elseif x == 5 and y == 3 then x = x - 1
        end
      elseif move == "R" then
        if x == 4 and y == 3 then x = x + 1
        elseif (x == 2 or x == 3) and (y == 2 or y == 3 or y == 4) then x = x + 1
        elseif x == 1 and y == 3 then x = x + 1
        end
      end
    end
    out = out .. KEYPAD2[y][x]
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
    io.stdout:write(part2(instructions), "\n\n")
  end
end

main()
