local m = {}

m.Bot = {}

function m.Bot.new(name)
  local o = {name = name, chips = {n = 0}}
  setmetatable(o, {__index = m.Bot})
  return o
end

function m.Bot:add_chip(chip)
  if self.chips.n == 2 then
    error("Trying to add a third chip")
  end
  self.chips[chip] = true
  self.chips.n = self.chips.n + 1
end

function m.Bot:remove_chip(chip)
  self.chips[chip] = nil
  self.chips.n = self.chips.n - 1
end

function m.Bot:add_rule(low, high) self.rule = {low = low, high = high} end
function m.Bot:has_both(one, two)
  return self.chips[one] and self.chips[two] and true or false
end

function m.Bot:get_chips()
  local out = {}
  for chip, _ in pairs(self.chips) do
    if chip ~= "n" then table.insert(out, chip) end
  end
  return table.unpack(out)
end

function m.Bot:execute_rule(bots)
  if self.chips.n < 2 then return false end
  local c1, c2 = self:get_chips()
  local low, high = math.min(c1, c2), math.max(c1, c2)

  bots[self.rule.low]:add_chip(low)
  bots[self.rule.high]:add_chip(high)
  self:remove_chip(low)
  self:remove_chip(high)
  return true
end

function m.Bot:is_bot() return self.name:find("^bot") end

function m.Bot:to_string()
  local rule = ""
  if self.rule ~= nil then
    rule = string.format(", giving low to %s and high to %s", self.rule.low, self.rule.high)
  end
  return string.format(
    "%s with chips [%s]%s",
    self.name,
    table.concat({self:get_chips()}, ", "),
    rule)
end


return m
