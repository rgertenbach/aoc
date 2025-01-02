TOTAL = 150

local f = assert(io.open("input.txt"))
local containers = {}
for container in f:lines() do
  table.insert(containers, tonumber(container))
end

table.sort(containers)

local cache = {}
local function dp(remaining, start)
  local key = string.format("%d,%d", remaining, start)
  if cache[key] ~= nil then return cache[key] end
  if remaining == 0 then
    cache[key] = 1
    return cache[key]
  end
  if remaining < 0 or start > #containers then
    cache[key] = 0
    return cache[key]
  end
  cache[key] = (
    dp(remaining - containers[start], start + 1) +
    dp(remaining, start + 1)
  )
  return cache[key]
end

print(dp(TOTAL, 1))
