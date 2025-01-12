package.path = "../lua/?.lua;" .. package.path

local md5 = require("md5")
local grid = require("grid")
local tbl = require("tbl")

local test_input = "ihgpwlah"
local input = "pslxynzg"
local passcode = input

---@param passcode string
---@param path string
---@return table<Direction, boolean> is_open
local function door_state(pc, path)
  local hash = md5.sumhexa(pc .. path)
  local out = {}
  out[grid.Direction.NORTH] = ("bcdef"):find(hash:sub(1, 1)) ~= nil
  out[grid.Direction.SOUTH] = ("bcdef"):find(hash:sub(2, 2)) ~= nil
  out[grid.Direction.WEST] = ("bcdef"):find(hash:sub(3, 3)) ~= nil
  out[grid.Direction.EAST] = ("bcdef"):find(hash:sub(4, 4)) ~= nil
  return out
end

local frontier = {{0, 0, ""}}

local movename = {}
movename[grid.Direction.NORTH] = "U"
movename[grid.Direction.SOUTH] = "D"
movename[grid.Direction.WEST] = "L"
movename[grid.Direction.EAST] = "R"

local best = 0

while #frontier > 0 do
  local next_frontier = {}
  for p in tbl.valuesi(frontier) do
    local cr, cc, path = p[1], p[2], p[3]
    if cr == 3 and cc == 3 then best = #path
    else
      local is_open = door_state(passcode, path)
      for direction in tbl.valuesi(grid.Direction) do
        local pr, pc = grid.move(cr, cc, direction)
        if is_open[direction] and pr >= 0 and pr < 4 and pc >= 0 and pc < 4 then
          table.insert(next_frontier, {pr, pc, path .. movename[direction]})
        end
      end
    end
  end
  frontier = next_frontier
end
print(best)
