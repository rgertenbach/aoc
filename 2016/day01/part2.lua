package.path = "../lua/?.lua;" .. package.path
local str = require("str")
local tbl = require("tbl")
local grid = require("grid")

---@alias Point [integer, integer]
---@alias Line [integer, integer, integer, integer]

---@param instructions string
---@return integer, integer Point The xy coordinates of the first intersection.
local function follow_tape(instructions)
  local visited = {["0,0"] = true}
  local x, y = 0, 0
  local orientation = grid.Direction.NORTH
  for instruction in tbl.valuesi(str.split(instructions, ", ")) do
    local turdir = (string.sub(instruction, 1, 1) == "R") and grid.Turn.CLOCKWISE or grid.Turn.COUNTERCLOCKWISE
    orientation = grid.turn(orientation, turdir)
    for _ = 1, tonumber(instruction:sub(2)) do
      x, y = grid.move(x, y, orientation)
      local f = string.format("%d,%d", x, y)
      if visited[f] then return x, y end
      visited[f] = true
    end

  end
  return x, y
end

local function main()
  local file = io.open("input.txt")
  if file == nil then
    return
  end
  local instructions = file:read("l")
  local x, y = follow_tape(instructions)
  x = math.abs(x)
  y = math.abs(y)
  print(x+y)
  file:close()
end

main()
