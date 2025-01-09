package.path = "/home/robin/src/aoc/2016/lua/?.lua;" .. package.path
local grid = require("grid")
local tbl = require("tbl")

local input = 1362
local test_input = 10


---@param row integer
---@param col integer
---@param fav integer
---@return boolean
local function iswall(row, col, fav)
  local f = col*col + 3*col + 2*col*row + 1*row + row*row
  f = f + fav
  local n = 0
  while f > 0 do
    n = n + f & 1
    f = f >> 1
  end
  return n % 2 == 1
end

---@param row integer
---@param col integer
---@return string key
local function make_key(row, col)
  return string.format("%d,%d", row, col)
end

---@param f fun(row: integer, col: integer, fav: integer): boolean
---@param fav integer
---@return integer steps
local function steps(f, fav)
  local visited = {["1,1"] = true}
  local boundary = {{1,1}}
  local taken = 0
  while #boundary > 0 do
    local new_boundary = {}
    for _, point in ipairs(boundary) do
      local row, col = table.unpack(point)
      for _, dir in pairs(grid.Direction) do
        local pr, pc = grid.move(row, col, dir)
        local pkey = make_key(pr, pc)
        if pr >= 0 and pc >= 0 and not f(pr, pc, fav) and not visited[pkey] then
          visited[pkey] = true
          table.insert(new_boundary, {pr, pc})
        end
      end
    end
    taken = taken + 1
    boundary = new_boundary
    if taken == 50 then break end
  end
  local nvisited = 0
  for _, _ in pairs(visited) do
    nvisited = nvisited + 1
  end
  return nvisited
end

print(steps(iswall, input))

