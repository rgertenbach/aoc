local M = {}

---@enum Direction
M.Direction = {
  NORTH = 270,
  EAST = 0,
  SOUTH = 90,
  WEST = 180,
}

---@enum Turn
M.Turn = {
  STRAIGHT = 0,
  CLOCKWISE = 90,
  REVERSE = 180,
  COUNTERCLOCKWISE = -90,
}

---Turns an orientation.
---@param dir Direction
---@param rot Turn
function M.turn(dir, rot)
  return (dir + 360 + rot) % 360
end

---Moves into a direction.
---@param row integer
---@param col integer
---@param dir Direction
---@param amt integer?
---@return integer, integer rc
function M.move(row, col, dir, amt)
  amt = amt or 1
  if dir == M.Direction.NORTH then return row - amt, col end
  if dir == M.Direction.EAST then return row, col + amt end
  if dir == M.Direction.SOUTH then return row + amt, col end
  if dir == M.Direction.WEST then return row, col - amt end
  error(string.format("Unknown direction: '%s'", dir))
end



return M
