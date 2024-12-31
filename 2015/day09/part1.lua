local f = assert(io.open("input.txt"))

local links = {}

for line in f:lines() do
  local a, b, d = line:match("^(%w+) to (%w+) = (%d+)$")
  if links[a] == nil then links[a] = {} end
  if links[b] == nil then links[b] = {} end
  links[a][b] = tonumber(d)
  links[b][a] = tonumber(d)
end

local spots = {}
for spot, _ in pairs(links) do table.insert(spots, spot) end


---@param current integer
---@param visited integer
---@return integer
local function dfs(current, visited)
  local best = math.huge
  for i = 1, #spots do
    if (1 << (i - 1)) & visited == 0 then
      local d = links[spots[current]][spots[i]]
      local nv = visited | (1 << (i - 1))
      if nv == (1 << #spots) - 1 then return d end
      local n = dfs(i, nv)
      if d + n < best then best = d + n end
    end
  end
  return best
end

local best = math.huge
for current = 1, #spots do
  local d = dfs(current, (1 << (current - 1)))
  if d < best then best = d end
end
print(best)

