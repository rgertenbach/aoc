--- 3 groups, same weight, needs to "fit"
--- Group 1 needs as few packages as possible
--- Among those that have the fewest packages we need to limit the product
--- This means we want to put one heavy one and a few small ones

---@param t number[]
---@return number
local function sum(t)
  local total = 0
  for _, x in ipairs(t) do total = total + x end
  return total
end

---@param t number[]
---@return number
local function product(t)
  local total = 1
  for _, x in ipairs(t) do total = total * x end
  return total
end

---@generic T
---@param t T[]
---@param x T
---@return boolean
local function contains(t, x)
  for _, y in ipairs(t) do
    if x == y then return true end
  end
  return false
end

local f = assert(io.open("input.txt"))
local gifts = {}
for line in f:lines() do table.insert(gifts, tonumber(line)) end
local n = gifts
local total_weight = sum(gifts)
local weight_per_group = total_weight // 3
f:close()
print("Searching sums to", weight_per_group)

---@param candidates integer[]
---@param target integer
---@return integer[][] sat arrays that sum to the target.
local function find_sums_to(candidates, target)
  local out = {}
  if target < 0 then return {{}} end
  for i, x in ipairs(candidates) do
    if x > target then break end
    if x == target then
      table.insert(out, {x})
      break
    end
    local new_candidates = {}
    for _, nc in ipairs(candidates) do
      if nc > x then table.insert(new_candidates, nc) end
    end
    for _, nxt in ipairs(find_sums_to(new_candidates, target - x)) do
      if #nxt > 0 and nxt[1] > x then
        table.insert(nxt, x)
        table.sort(nxt)
        table.insert(out, nxt)
      end
    end
  end
  return out
end

local function intersect(a, b)
  local lookup = {}
  for _, x in ipairs(b) do lookup[x] = true end
  for _, x in ipairs(a) do
    if lookup[x] then return true end
  end
  return false
end

---@param grp1 integer[]
---@param candidates integer[][]
---@return boolean Fit Wheter it fits.
local function fits(grp1, candidates)
  for _, grp2 in ipairs(candidates) do
    if not intersect(grp1, grp2) then return true end
  end
  return false
end


local candidates = find_sums_to(gifts, weight_per_group)
table.sort(candidates, function(a, b)
  if #a < #b then return true end
  if #a == #b then return product(a) < product(b) end
  return false
end)
for _, candidate in ipairs(candidates) do
  if fits(candidate, candidates) then
    print(product(candidate))
    break
  end
end
print(best_entanglement)

-- 4314250110705
-- 228451138763  -- too high
