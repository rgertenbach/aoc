GOAL = 29000000
--      1740000
--       665280
local current = 3

---@param upto integer
---@return integer[]
local function sieve(upto)
  local primes = {2}
  while current < upto do
    local i = 1
    while primes[i]^2 <= current do
      if current % primes[i] == 0 then break end
      i = i + 1
    end
    if current % primes[i] ~= 0 then
      table.insert(primes, current)
    end
    current = current + 2
  end
  return primes
end

PRIMES = sieve(GOAL // 5)

print("Done primes")

---@param x integer
---@return integer[]
local function prime_factors(x)
  local out = {}
  for _, prime in ipairs(PRIMES) do
    if prime > x then break end
    while x % prime == 0 do
      table.insert(out, prime)
      x = x // prime
    end
  end
  return out
end

---@param factors integer[]
---@param i integer?
---@return integer[]
local function products(factors, i)
  i = i or 1
  if i > #factors then return {1} end
  local p = {}
  for _, c in ipairs(products(factors, i + 1)) do
    p[c] = true
    p[c * factors[i]] = true
  end

  local out = {}
  for x, _ in pairs(p) do table.insert(out, x) end
  return out
end

---@param house integer
---@return integer
local function presents_at_house(house)
  local presents = 0
  for _, x in ipairs(products(prime_factors(house))) do
    if house // x <= 50 then 
      presents = presents + x * 11
    end
  end

  return presents
end

local n = 1
while presents_at_house(n) < GOAL do
  n = n + 1
  if n % (GOAL // 100) == 0 then print(n) end
end
print(n)

--2636369 too high
