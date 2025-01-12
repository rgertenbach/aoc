SAFE = "."
TRAP = "^"

---@param x integer which position.
---@param above string The row above.
local function is_trap(x, above)
  local left = x > 1 and above:sub(x - 1, x - 1) == TRAP
  local center = above:sub(x, x) == TRAP
  local right = x < #above and above:sub(x + 1, x + 1) == TRAP
  return (
    (left and center and not right) or
    (center and right and not left) or
    (left and not center and not right) or
    (right and not left and not center)
  )
end


---@param row string
---@return string row
local function extend(row)
  local out = {}
  for i = 1, #row do
    table.insert(out, is_trap(i, row) and TRAP or SAFE)
  end
  return table.concat(out)
end

---@param row string
---@return integer
local function count_safe(row)
  return #row - #row:gsub("%" .. SAFE, "")
end


local f = assert(io.open("input.txt"))
local current = f:read("l")
f:close()
local safe = 0
local rows = 0

while rows < 400000 do
  safe = safe + count_safe(current)
  current = extend(current)
  rows = rows + 1
end
print(safe)
