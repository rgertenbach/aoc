package.path = "/home/robin/src/aoc/2016/lua/?.lua;" .. package.path


local md5 = require("md5")

local input = "yjdafjpo"
local test_input = "abc"

---@param s string
---@param n integer
---@return string? The character that repeats n times
local function repeatsn(s, n)
  local last = ''
  local run = 0
  for i = 1, #s do
    if s:sub(i, i) == last then
      run = run + 1
      if run == n then return s:sub(i, i) end
    else
      last = s:sub(i, i)
      run = 1
    end
  end
  return nil
end

---@param i integer
---@param salt string
---@return string hash
local function hash(i, salt)
  return md5.sumhexa(string.format("%s%d", salt, i))
end

---@class Key
---@field i integer
---@field key string
---@field c string The triple character.

---@param i integer
---@param salt string
---@return Key key
local function next_key(i, salt)
  while true do
    local key = hash(i, salt)
    if repeatsn(key, 3) then return {i=i, key=key, c=repeatsn(key, 3)} end
    i = i + 1
  end
end

local salt = input
local current_builder_triple = next_key(0, salt)
local triples = {current_builder_triple}
local keys = {}


local triplei = 1
while #keys < 64 do
  local ch = triples[triplei]
  local triplek = triplei + 1
  while true do
    while #triples < triplek do
      current_builder_triple = next_key(current_builder_triple.i + 1, salt)
      table.insert(triples, current_builder_triple)
    end
    if triples[triplek].i - ch.i > 1000 then break end
    if string.find(triples[triplek].key, string.rep(ch.c, 5)) then
      table.insert(keys, ch)
      print(string.format("%d at index %d", #keys, keys[#keys].i))
      break
    end
    triplek = triplek + 1
  end

  triplei = triplei + 1
end

