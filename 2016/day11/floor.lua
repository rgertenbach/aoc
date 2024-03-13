local part = require("part")
local old_package_path = package.path
package.path = "../utils/?.lua;" .. package.path
local string_utils = require("string_utils")

local m = {}

---@class Floor Represents a floor in the warehouse.
m.Floor = {}

function m.Floor:new(o)
  o = o or {}
  self.__index = self
  setmetatable(o, self)
  return o
end

function m.Floor:parse(s)
  s = s:gsub("The %w+ floor contains ", "")
  s = s:gsub(".$", "")
  s = s:gsub(" and ", ", ")
  s = s:gsub("a ", "")
  local parts = string_utils.split(s, ", ")
  if parts[1] == "nothing relevant" then return self:new() end
  local out = {}
  for _, p in ipairs(parts) do
    table.insert(out, part.Part:parse(p))
  end
  return self:new(out)
end

function m.Floor:to_string()
  local sparts = {}
  for _, p in ipairs(self) do
    table.insert(sparts, p:to_string(p))
  end
  return table.concat(sparts, "  ")
end

package.path = old_package_path
return m
