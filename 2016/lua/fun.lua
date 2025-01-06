local M = {}

---@generic T1
---@generic T2
---@param f fun(x: T1, ...): T2
---@param xs T1[]
---@param ... any
---@return T2[]
function M.map(f, xs, ...)
  local out = {}
  for _, x in ipairs(xs) do table.insert(out, f(x, ...)) end
  return out
end

return M
