BOSSHP = 71
BOSSDMG = 10
HP = 50
MANA = 500
-- BOSSHP = 13 -- 226
-- BOSSHP = 14 -- 641
-- BOSSDMG = 8
-- HP = 10
-- MANA = 250

local function copy(t)
  local out = {}
  for k, v in pairs(t) do out[k] = v end
  return out
end

---@class State
---@field spent integer
---@field hp integer
---@field mana integer
---@field boss integer
---@field shield integer
---@field poison integer
---@field recharge integer

---@return State
local function State(spent, hp, mana, boss, shield, poison, recharge)
  return {
    spent=spent,
    hp=hp,
    mana=mana,
    boss=boss,
    shield=shield,
    poison=poison,
    recharge=recharge,
  }
end

---@type State[]
local heap = {State(0, HP, MANA, BOSSHP, 0, 0, 0)}

---@param s State
local function apply_effects(s)
  if s.poison > 0 then
    s.boss = s.boss - 3
    s.poison = s.poison - 1
  end

  if s.recharge > 0 then
    s.mana = s.mana + 101
    s.recharge = s.recharge - 1
  end

  if s.shield > 0 then s.shield = s.shield - 1 end
end

local function fstate(s)
  local out = {}
  for k, v in pairs(s) do
    table.insert(out, string.format("%s:%d", k, v))
  end
  return table.concat(out, ",")
end

local handled_states = {}

local function bossattack(s)
  local shield = s.shield > 0 and 7 or 0
  local dmg = math.max(1, BOSSDMG - shield)
  s.hp = s.hp - dmg
end

while #heap > 0 do
  table.sort(heap, function(a, b) return b.spent < a.spent end)

  local s = table.remove(heap) ---@type State
  apply_effects(s)

  if s.boss <= 0 then
    print(s.spent)
    break
  end

  -- Magic Missile
  if s.mana >= 53 then
    local new = copy(s)
    new.spent = new.spent + 53
    new.mana = new.mana - 53
    new.boss = new.boss - 4
    apply_effects(new)
    if new.boss <= 0 then
      print(new.spent)
      break
    end
    bossattack(new)
    local f = fstate(new)
    if new.hp > 0 and handled_states[f] == nil then
      handled_states[f] = true
      table.insert(heap, new)
    end
  end

  -- Drain
  if s.mana >= 73 then
    local new = copy(s)
    new.spent = new.spent + 73
    new.mana = new.mana - 73
    new.boss = new.boss - 2
    new.hp = new.hp + 2
    apply_effects(new)
    if new.boss <= 0 then
      print(new.spent)
      break
    end
    bossattack(new)
    local f = fstate(new)
    if new.hp > 0 and handled_states[f] == nil then
      handled_states[f] = true
      table.insert(heap, new)
    end
  end

  -- Shield
  if s.mana >= 113 and s.shield == 0 then
    local new = copy(s)
    new.spent = new.spent + 113
    new.mana = new.mana - 113
    new.shield = 6
    apply_effects(new)
    if new.boss <= 0 then
      print(new.spent)
      break
    end
    bossattack(new)
    local f = fstate(new)
    if new.hp > 0 and handled_states[f] == nil then
      handled_states[f] = true
      table.insert(heap, new)
    end
  end


  -- Poison
  if s.mana >= 173 and s.poison == 0 then
    local new = copy(s)
    new.spent = new.spent + 173
    new.mana = new.mana - 173
    new.poison = 6
    apply_effects(new)
    if new.boss <= 0 then
      print(new.spent)
      break
    end
    bossattack(new)
    local f = fstate(new)
    if new.hp > 0 and handled_states[f] == nil then
      handled_states[f] = true
      table.insert(heap, new)
    end
  end

  -- Recharge
  if s.mana >= 229 and s.recharge == 0 then
    local new = copy(s)
    new.spent = new.spent + 229
    new.mana = new.mana - 229
    new.recharge = 5
    apply_effects(new)
    if new.boss <= 0 then
      print(new.spent)
      break
    end
    bossattack(new)
    local f = fstate(new)
    if new.hp > 0 and handled_states[f] == nil then
      handled_states[f] = true
      table.insert(heap, new)
    end
  end
end

--1957 too high
