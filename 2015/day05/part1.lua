---@param s string
local function is_nice(s)
  if s:len() - s:gsub("[aeiou]", ""):len() < 3 then return false end
  local has_double = false
  for i = 1, #s-1 do
    if s:sub(i, i) == s:sub(i+1, i+1) then
      has_double = true
      break
    end
  end
  if not has_double then return false end
  if s:find("ab") then return false end
  if s:find("cd") then return false end
  if s:find("pq") then return false end
  if s:find("xy") then return false end
  return true
end

local f = assert(io.open("input.txt"))
local nice = 0
for line in f:lines() do
  if is_nice(line) then nice = nice + 1 end
end
print(nice)
