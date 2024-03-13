local m = {}

--- Defaultdict like in python
---@param constructor function A niladic function constructing default value.
---@param pass_key boolean Whether to pass the field name into the constructor
---   or not. This can be helpful when the constructor is a class constructor
---   needs to be aware of its own key.
---@return table A table that acts like a defaultdict.
function m.defaultdict(constructor, pass_key)
  local out = {}
  local mt = {
    __index = function(t, f)
      local val = rawget(t, f) or constructor(pass_key and f)
      rawset(t, f, val)
      return val
    end
  }
  setmetatable(out, mt)
  return out
end

return m
