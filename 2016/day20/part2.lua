MAX_IP = 4294967295
local blocklist = {}

local f = assert(io.open("input.txt"))

for line in f:lines() do
  local s, e = line:match("^(%d+)-(%d+)$")
  table.insert(blocklist, {tonumber(s), tonumber(e)})
end

f:close()

table.sort(blocklist, function(a, b)
  return a[1] < b[1] or a[1] == b[1] and a[2] < b[2]
end)

local allowed = 0
local last_e = 0

for _, b in ipairs(blocklist) do
  allowed = allowed + math.max(0, b[1] - last_e - 1)
  last_e = math.max(last_e, b[2])
end
allowed = allowed + math.max(0, MAX_IP - last_e - 1)


print(allowed)
