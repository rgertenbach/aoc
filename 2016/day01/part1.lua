package.path = "../lua/?.lua;" .. package.path
local str = require("str")
local tbl = require("tbl")
local grid = require("grid")

local function follow_instruction(instruction, x, y, orientation)
  local rotation = (
    string.sub(instruction, 1, 1) == "R"
    and grid.Turn.CLOCKWISE
    or grid.Turn.COUNTERCLOCKWISE)
  local steps = tonumber(string.sub(instruction, 2))
  orientation = grid.turn(orientation, rotation)
  y, x = grid.move(y, x, orientation, steps)
  return x, y, orientation
end

local function follow_tape(instructions, x, y, orientation)
  for instruction in tbl.valuesi(str.split(instructions, ", ")) do
    x, y, orientation = follow_instruction(instruction, x, y, orientation)
  end
  return x, y, orientation
end

local function main()
  local file = io.open("input.txt")
  if file == nil then
    return
  end
  local instructions = file:read("l")
  local x, y = follow_tape(instructions, 0, 0, grid.Direction.NORTH)
  x = math.abs(x)
  y = math.abs(y)
  print(x + y)
  file:close()
end

main()
