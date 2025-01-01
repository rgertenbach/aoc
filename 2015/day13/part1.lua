local f = assert(io.open("input.txt"))

local happy = {}
for line in f:lines() do
  local a, d, h, b = line:match("^(%w+) would (%w+) (%d+) happiness units by sitting next to (%w+).$")
  if happy[a] == nil then happy[a] = {} end
  h = tonumber(h)
  if d == "lose" then h = -h end
  happy[a][b] = h
end

local people = {}
for p, _ in  pairs(happy) do
  table.insert(people, p)
end

---@param current integer Latest person placed.
---@param seated integer Bitmask of placed people.
local function dfs(current, seated)
  local best = 0
  for i = 2, #people do
    local new_seated = seated | (1 << (i -  1))
    if new_seated > seated then
    local current_happiness = 0
      current_happiness = current_happiness + happy[people[current]][people[i]]
      current_happiness = current_happiness + happy[people[i]][people[current]]
      if new_seated == (1 << (#people)) -  1 then
        current_happiness = current_happiness + happy[people[i]][people[1]]
        current_happiness = current_happiness + happy[people[1]][people[i]]
        return current_happiness
      end
      current_happiness = current_happiness + dfs(i, new_seated)
      if current_happiness  > best then best = current_happiness end
    end
  end
  return best
end

print(dfs(1, 1))
