package.path = "../utils/?.lua;" .. package.path
local su = require("string_utils")

---@param s string the input
local function is_palindrome(s) return s == s:reverse() end
local function is_abba(s)
  for start = 1, #s - 3 do
    local a, b = s:sub(start+0, start+0), s:sub(start+1, start+1)
    local c, d = s:sub(start+2, start+2), s:sub(start+3, start+3)
    if a ~= b and a == d and b == c then return true end
  end
  return false
end

local function supports_tls(s)
  for _, hns in ipairs(s.hnss) do
    if is_abba(hns) then return false end
  end
  for _, com in ipairs(s.coms) do
    if is_abba(com) then return true end
  end
  return false
end


---@param s string The IP
---@return table[string, string] A table with the ip components (com) and hypernet sequence (hns)
local function parse(s)
  local out = {hnss = {}}
  local pat = "%[(.-)%]"
  for m in s:gmatch(pat) do table.insert(out.hnss, m) end
  out.coms = su.split(s:gsub(pat, ","), ",")
  return out
end

for i = 1, #arg do
  io.stdout:write(arg[i], "\n")
  local file = assert(io.open(arg[i], "r"))
  local p1 = 0
  for line in file:lines() do
    local p = parse(line)
    if supports_tls(p) then p1 = p1 + 1 end
  end
  io.stdout:write(string.format("  Part1: %d", p1), "\n")
  file:close()
end
