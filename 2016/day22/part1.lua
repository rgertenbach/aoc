local f = assert(io.open("input.txt"))


_ = f:read("l")
_ = f:read("l")

---@class Node
---@field size integer
---@field used integer

local nodes = {}  ---@type table<string,  Node>


local function key(x, y)
  return string.format("%d,%s", x, y)
end

for line in f:lines() do
  local x, y, size, used = line:match("^/dev/grid/node%-x(%d+)%-y(%d+) *(%d+)T *(%d+).*")
  x, y, size, used = tonumber(x), tonumber(y), tonumber(size), tonumber(used)
  nodes[key(x, y)] = {size=size, used=used}
end

local viable = 0
for ak, av in pairs(nodes) do
  for bk, bv in pairs(nodes) do
    if ak ~= bk then
      if av.used > 0 and bv.size - bv.used >= av.used then
        viable = viable + 1
      end
    end
  end
end

print(viable)
