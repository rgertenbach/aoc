local f = assert(io.open("input.txt"))


---@class Ingredient
---@field capacity integer
---@field durability integer
---@field flavor integer
---@field texture integer
---@field calories integer

---@class Cookie
---@field capacity integer
---@field durability integer
---@field flavor integer
---@field texture integer
---@field calories integer
local Cookie = {}

local values = {}
local ingredients = {}

---@param capacity integer?
---@param durability integer?
---@param flavor integer?
---@param texture integer?
---@param calories integer?
---@return Cookie
function Cookie:new(capacity, durability, flavor, texture, calories)
  local t = {
    capacity = capacity or 0,
    durability = durability or 0,
    flavor = flavor or 0,
    texture = texture or 0,
    calories = calories or 0,
  }
  self.__index = self
  setmetatable(t, Cookie)
  return t
end

---@return Cookie
function Cookie:copy()
  local out = {}
  for k, v in pairs(self) do
    out[k] = v
  end
  setmetatable(out, Cookie)
  return out
end

---@param ingredient Ingredient
---@param amount integer
---@return Cookie
function Cookie:add(ingredient, amount)
  local new = self:copy()
  for k, amt in pairs(self) do
    new[k] = amt + amount * ingredient[k]
  end
  return new
end

---@return integer
function Cookie:value()
  local out = 1
  for key, x in pairs(self) do
    if x <= 0 then return 0 end
    if key ~= "calories" then out = out * x end
  end
  return out
end

function Cookie:print(ostream)
  ostream = ostream or io.stdout
  local fstring = "Cap: %d\nDur: %d\nFla: %d\nTex: %d\nCal: %d\nVal: %d\n"
  local out = fstring:format(
    self.capacity, self.durability, self.flavor,
    self.texture, self.calories, self:value()
  )
  ostream:write(out)
end


for line in f:lines() do
  local name, capacity, durability, flavor, texture, calories =
    line:match("^(%w+): capacity (%-?%d+), durability (%-?%d+), flavor (%-?%d+), texture (%-?%d+), calories (%-?%d+)$")
  values[name] = {
    capacity = tonumber(capacity),
    durability = tonumber(durability),
    flavor = tonumber(flavor),
    texture = tonumber(texture),
    calories = tonumber(calories)
  }
  table.insert(ingredients, name)
end
f:close()

---@param ingredient integer Which ingredient to add.
---@param used integer How many spoons / 100 have been used already.
---@param sofar Cookie The Cookie so far.
---@return Cookie A cookie with maximum value.
local function foo(ingredient, used, sofar)
  local vals = values[ingredients[ingredient]]
  if ingredient == #ingredients then
    return sofar:add(vals, 100 - used)
  end
  local best_cookie = Cookie:new()
  for amt = 1, 100 - used - (#ingredients - ingredient) do
    local best_sub = foo(ingredient + 1, used + amt, sofar:add(vals, amt))
    if best_sub:value() > best_cookie:value() and best_sub.calories == 500 then
      best_cookie = best_sub
    end
  end
  return best_cookie
end

print(foo(1, 0, Cookie:new()):value())
