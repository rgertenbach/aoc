---@param s string
local function xxabcxx(s)
  local pairs = {}
  for i = 1, #s-1 do
    local sub = s:sub(i, i+1)
    if pairs[sub] and pairs[sub] < i - 1 then return true end
    pairs[sub] = i
  end
  return false
end

---
---@param s string
local function xyx(s)
  for i = 1, #s - 2 do
    if s:sub(i, i) == s:sub(i + 2, i + 2) then return true end
  end
  return false
end

---@param s string
local function is_nice(s)
  return xxabcxx(s) and xyx(s)
end

local f = assert(io.open("input.txt"))
local nice = 0
for line in f:lines() do
  if is_nice(line) then nice = nice + 1 end
end
print(nice)
