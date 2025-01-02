TOTAL = 150

local f = assert(io.open("input.txt"))
local jugs = {}
for container in f:lines() do
  table.insert(jugs, tonumber(container))
end

---@param i integer?
---@return integer[]
local function make_count(i)
  local freq = {}
  for _ = 1, #jugs do table.insert(freq, 0) end
  if i then freq[i] = 1 end
  return freq
end

---@param a integer[]
---@param b integer[]
---@return integer[]
local function addfreq(a, b)
  local out = {}
  for i = 1, #jugs do out[i] = a[i] + b[i] end
  return out
end

local cache = {}

---@param rem integer Amount remaining.
---@param i integer start position.
---@param k integer jugs used so far.
---@return integer[]
local function dp(rem, i, k)
  local key = string.format("%d,%d,%d", rem, i, k)
  if cache[key] ~= nil then return cache[key] end
  if rem == 0 then cache[key] = make_count(k)
  elseif rem < 0 or i > #jugs then cache[key] = make_count()
  else cache[key] = addfreq(dp(rem - jugs[i], i + 1, k + 1), dp(rem, i + 1, k))
  end
  return cache[key]
end

local x = dp(TOTAL, 1, 0)

for i = 1, #jugs do
  print(i, x[i])
end
