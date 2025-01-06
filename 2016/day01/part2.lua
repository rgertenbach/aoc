package.path = "../lua/?.lua;" .. package.path
local str = require("str")
local tbl = require("tbl")
local grid = require("grid")

---@alias Point [integer, integer]
---@alias Line [integer, integer, integer, integer]

---@param instruction string
---@param x integer
---@param y integer
---@param orientation Direction
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

---TODO: Fix
---@param p1 Line
---@param p2 Line
---@return integer, integer
local function intersect(p1, p2)
  if p1[1] == p1[3] then  -- Vertical
    if p2[1] == p2[3] then -- Also vertical
      if p1[1] ~= p2[1] then return false end
      if p1[2] >= p2[2] and p1[2] <= p2[4] then return true end
      if p1[4] >= p2[2] and p1[4] <= p2[4] then return true end
      if p2[2] >= p1[2] and p2[2] <= p1[4] then return true end
      if p2[4] >= p1[2] and p2[4] <= p1[4] then return true end
      return false
    end
    return false
    -- Crossing
  end
  if p1[2] == p1[4] then  -- Horizontal
    if p2[2] == p2[4] then -- Also Horizontal
      if p1[2] ~= p2[2] then return false end

      if p1[1] >= p2[1] and p1[1] <= p2[4] then return true end
      if p1[3] >= p2[1] and p1[3] <= p2[4] then return true end
      if p2[1] >= p1[1] and p2[1] <= p1[4] then return true end
      if p2[3] >= p1[1] and p2[3] <= p1[4] then return true end
    end
  end
  return false
end

---@param paths Line[]
---@param path Line
---@return integer, integer
local function any_intersect(paths, path)
  for _, other in ipairs(paths) do
    local int_x, int_y = intersect(other, path)
    if int_x then return int_x, int_y end
  end
  return nil
end

---@param instructions string
---@param x integer column
---@param y integer row
---@param orientation Direction
---@return integer, integer, Direction
local function follow_tape(instructions, x, y, orientation)
  local paths = {}
  for instruction in tbl.valuesi(str.split(instructions, ", ")) do
    local old_x, old_y = x, y
    x, y, orientation = follow_instruction(instruction, x, y, orientation)
    local path  = {old_x, old_y, x, y}
    local int_x, int_y = any_intersect(paths, path)
    if int_x then return int_x, int_y, orientation end
    paths[#paths] = path
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
  print(x)
  file:close()
end

main()
