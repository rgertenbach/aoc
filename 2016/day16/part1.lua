---@param x string
---@param n integer
local function fill(x, n)
  while #x < n do
    local suffix = x:reverse():gsub("0", "9"):gsub("1", "0"):gsub("9", "1")
    x = x .. "0" .. suffix
  end
  return x:sub(1, n)
end

---
---@param x string
local function checksum(x)
  local pairs = {}
  for i = 1, #x-1, 2 do
    if x:sub(i, i) == x:sub(i+1, i+1) then table.insert(pairs, "1")
    else table.insert(pairs, "0")
    end
  end
  local out = table.concat(pairs)
  if #out % 2 == 0 then return checksum(out) end
  return out
end

print(checksum(fill("10011111011011001", 272)))
