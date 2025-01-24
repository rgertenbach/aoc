-- Read file
-- find distances between points
-- find shortest permutation
package.path = "/home/robin/src/llib/lua/?.lua;" .. package.path
local tbl = require("tbl")

local f = assert(io.open("input.txt"))

local function key(row, col)
  return string.format("%d,%d", row, col)
end

local function permutations(n, current, set)
  local out = {}
  if set == (1 << n) - 1 then
    return {current}
  end
  for i = 1, n do
    if set & (1 << (i - 1)) == 0 then
      local temp = {}
      for v in tbl.ivalues(current) do table.insert(temp, v) end
      table.insert(temp, i)
      for v in tbl.ivalues(permutations(n, temp, set | (1 << (i - 1)))) do
        table.insert(out, v)
      end
    end
  end
  return out
end

local map = {}
local targets = {}
local walls = {}

for line in f:lines() do
  table.insert(map, line)
end
f:close()

local rows = #map
local cols = #map[1]


for row, line in ipairs(map) do
  for col = 1, #line do
    local c = line:sub(col, col)
    if c == "#" then walls[key(row, col)] = true
    elseif c ~= "." then
      local target = assert(tonumber(c))
      targets[target] = {row, col}
    end
  end
end

local targets_by_address = {}
local distances = {}   --- @type table<string, integer>

for i, target in pairs(targets) do
  targets_by_address[key(target[1], target[2])] = i
end

for i, start in pairs(targets) do
  local visited = {}
  visited[key(start[1], start[2])] = true
  local queue = {{start[1], start[2]}}
  local steps = 0
  while #queue > 0 do
    local next_queue = {}
    for current in tbl.ivalues(queue) do
      local cr, cc = current[1], current[2]

      if targets_by_address[key(cr, cc)] ~= nil then
        distances[key(i, targets_by_address[key(cr, cc)])] = steps
      end

      for prop in tbl.ivalues({{cr - 1, cc}, {cr + 1, cc}, {cr, cc-1}, {cr, cc+1}}) do
        local pr, pc = prop[1], prop[2]
        if pr <= 0 or pr > rows or pc <= 0 or pc > cols then goto continue
        elseif visited[key(pr, pc)] then goto continue
        elseif walls[key(pr, pc)] then goto continue
        end

        visited[key(pr, pc)] = true
        table.insert(next_queue, {pr, pc})

        ::continue::
      end  -- Proposed
    end  -- Current
    queue = next_queue
    steps = steps + 1
  end  -- Queue
end  -- Start

local best = math.huge
for perm in tbl.ivalues(permutations(#targets, {}, 0)) do
  local dist = 0
  local current = 0
  for tgt in tbl.ivalues(perm) do
    dist = dist + distances[key(current, tgt)]
    current = tgt
  end
  best = math.min(best, dist)
end
print(best)
