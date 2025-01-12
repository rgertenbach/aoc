package.path = "../lua/?.lua;" .. package.path

local tbl = require("tbl")

---@class Disc
---@field i integer Disc id.
---@field n integer Number of positions.
---@field p integer Current position.
---@field o integer Index adjusted position


---@param line string
---@return Disc
local function parse_line(line)
  local i, n, p = line:match("^Disc #(%d) has (%d+) positions; at time=0, it is at position (%d+).$")
  i, n, p = tonumber(i), tonumber(n), tonumber(p)
  local o = (p + i) % n
  return {i=i, n=n, p=p, o=o}
end

local discs = {}  ---@type Disc[]
local f = assert(io.open("input.txt"))
for line in f:lines() do
  local disc = parse_line(line)
  table.insert(discs, disc)
  print(disc.i, disc.n, disc.p, disc.o)
end


table.sort(discs, function(a, b) return a.n < b.n end)

---@param h integer heigh from which the ball is dropped.
---@param discs Disc[0]
local function falls(h, discs)
  for disc in tbl.valuesi(discs) do
    if (disc.o + h) % disc.n ~= 0 then return false end
  end
  return true
end

local guess = discs[#discs].n - discs[#discs].o
while not falls(guess, discs) do
  guess = guess + discs[#discs].n
end

print(guess)

