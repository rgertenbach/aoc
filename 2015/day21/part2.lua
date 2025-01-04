
---@class Unit
---@field hp integer
---@field dmg integer
---@field shield integer
---@field spent integer?

---@class Item
---@field cost integer
---@field dmg integer
---@field shield integer

---@return Item
local function make_item(cost, dmg, shield)
  return {cost=cost, dmg=dmg, shield=shield}
end

---@return Unit
local function make_unit(hp, dmg, shield, spent)
  return {hp=hp, dmg=dmg, shield=shield, spent=spent or 0}
end

---@type Item[]
local weapons = {
  make_item( 8, 4, 0),
  make_item(10, 5, 0),
  make_item(25, 6, 0),
  make_item(40, 7, 0),
  make_item(74, 8, 0)
}

---@type Item[]
local armor = {
  make_item( 13, 0, 1),
  make_item( 31, 0, 2),
  make_item( 53, 0, 3),
  make_item( 75, 0, 4),
  make_item(102, 0, 5)
}

---@type Item[]
local rings = {
  make_item( 25, 1, 0),
  make_item( 50, 2, 0),
  make_item(100, 3, 0),
  make_item( 20, 0, 1),
  make_item( 40, 0, 2),
  make_item( 80, 0, 3)
}

---@param player Unit
---@param boss Unit
local function wins(player, boss)
  while true do
    boss.hp = boss.hp - math.max(1, player.dmg - boss.shield)
    if boss.hp <= 0 then return true end
    player.hp = player.hp - math.max(1, boss.dmg - player.shield)
    if player.hp <= 0 then return false end
  end
end

---@type Unit[]
local players = {make_unit(100, 0, 0)}
for _, p in ipairs(players) do
  local new_players = {}
  for _, e in ipairs(weapons) do
    table.insert(
      new_players,
      make_unit(p.hp, p.dmg + e.dmg, p.shield + e.shield, p.spent + e.cost))
  end
  players = new_players
end


local new_players = {}
for _, p in ipairs(players) do
  table.insert(new_players, p)  -- Don't buy any
  for _, e in ipairs(armor) do
    table.insert(
      new_players,
      make_unit(p.hp, p.dmg + e.dmg, p.shield + e.shield, p.spent + e.cost))
  end
end
players = new_players

new_players = {}
for _, p in ipairs(players) do
  table.insert(new_players, p)  -- Don't buy any
  for i, e in ipairs(rings) do
    -- Buy one
    table.insert(
      new_players,
      make_unit(p.hp, p.dmg + e.dmg, p.shield + e.shield, p.spent + e.cost))
    for j, e2 in ipairs(rings) do
      if j > i then
        -- Buy two
        table.insert(
          new_players,
          make_unit(p.hp, p.dmg + e.dmg + e2.dmg, p.shield + e.shield + e2.shield, p.spent + e.cost + e2.cost))
      end
    end
  end
end
players = new_players

local most = 0  ---@type integer

for _, player in ipairs(players) do
  if not wins(player, make_unit(104, 8, 1)) and player.spent > most then
    most = player.spent
  end
end
print(most)

-- 176 too high
