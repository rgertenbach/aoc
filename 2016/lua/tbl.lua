local M = {}


---Iteator for values of a table
---@generic T
---@param t table<any, T>
---@return fun(): T
function M.valuesi(t)
  local last = nil
  local function iterator()
    local v
    last, v = next(t, last)
    return v
  end
  return iterator
end

---Iteator for keys of a table
---@generic T
---@param t table<T, any>
---@return fun(): T
function M.keysi(t)
  local last = nil
  local function iterator()
    last = next(t, last)
    return last
  end
  return iterator
end

---Values of a key-value table.
---@generic T
---@param t table<any, T>
---@return T[]
function M.values(t)
  local out = {}
  for v in M.valuesi(t) do table.insert(out, v) end
  return out
end

---Values of a key-value table.
---@generic T
---@param t table<T, any>
---@return T[]
function M.keys(t)
  local out = {}
  for v in M.keysi(t) do table.insert(out, v) end
  return out
end

--- Like Python's collections.defaultdict
---@generic K
---@generic V
---@param constructor fun(key: K): V Function constructing default value.
---@param pass_key boolean Whether to pass the field key into the constructor
---   or not. This can be helpful when the constructor is a class constructor
---   needs to be aware of its own key.
---@return table<K, V> Tbl A table that acts like a defaultdict.
function M.defaultdict(constructor, pass_key)
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

return M
