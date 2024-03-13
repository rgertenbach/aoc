local m = {}
m.part = require("part")
m.floor = require("floor")

---@class Warehouse
---@field floor string [public] The floow the elevator on.
m.Warehouse = {}

function m.Warehouse:new(floors)
  if floors == nil then
    error("Must pass a table with floors to Warehouse:new")
  end

  self.__index = self
  setmetatable(floors, self)
  floors.floor = 1
  return floors
end

function m.Warehouse:to_string()
  local floors = {}
  for i, floor in ipairs(self) do
    local elevator = (self.floor == i) and "E" or " "
    floors[5 - i] = string.format("F%d %s %s", i, elevator, floor:to_string())
  end
  return table.concat(floors, "\n")
end

return m
