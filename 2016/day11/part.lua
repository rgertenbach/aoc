local m = {}

---@enum PartType
m.PartType = {
  microchip = 1,
  generator = 2
}

---@class Part
---@field material string The type of material for the part.
---@field part_type PartType Whether the part is a chip or generator.
m.Part = {}

---Makes a new part
---@param o table A table setting the material and part_type
---@return Part
function m.Part:new(o)
  if o.material == nil then error("No material provided") end
  if o.part_type == nil then error("No part_type provided") end
  self.__index = self
  setmetatable(o, self)
  return o
end

---Parses a part
---@param s string The part to parse, liek "foo generator".
---@return Part 1 The first letter and whether it's a generator or chip.
function m.Part:parse(s)
  return self:new({
    material = s:match("^%w"):upper(),  -- First letter only.
    part_type = m.PartType[s:match("%w+$")],
  })
end

---Turns the part into a string.
---@return string A string representation of the part.
function m.Part:to_string()
  return string.format(
  "%s%s",
  self.material,
  self.part_type == m.PartType.microchip and "M" or "G")
end
return m
