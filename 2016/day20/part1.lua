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

local last_e = 0
local i = 1
while blocklist[i][1] <= last_e do
  last_e = math.max(last_e, blocklist[i][2])
  i = i + 1
end

print(last_e + 1)
