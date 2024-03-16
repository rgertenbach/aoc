package.path = "/home/robin/lua/lib/?.lua;" .. package.path

local rset = require "rset"
local rnamedtuple = require "rnamedtuple"
local rstring = require "rstring"
local Pos = rnamedtuple.namedtuple("Pos", {"x", "y"})
local hash = rnamedtuple.hash
local set = rset.set


local function parse_moves(s)
  local out = {}
  for e in rstring.split(s, "") do
    if e == "\n" then break end
    table.insert(out, e)
  end
  return out
end

local function load_moves(filename)
  local f = assert(io.open(filename, "r"))
  local line = f:read("l")
  return parse_moves(line)
end

local function move(current, dir)
  if     dir == ">" then return Pos{x = current.x + 1, y = current.y}
  elseif dir == "<" then return Pos{x = current.x - 1, y = current.y}
  elseif dir == "v" then return Pos{x = current.x, y = current.y + 1}
  elseif dir == "^" then return Pos{x = current.x, y = current.y - 1}
  else error("Unsupported direction: " .. dir)
  end
end

local function part1(moves)
  local pos = Pos{x = 0, y = 0}
  local visited = set()
  rset.add(visited, hash(pos))
  for _, dir in ipairs(moves) do
    pos = move(pos, dir)
    rset.add(visited, hash(pos))
  end
  return #visited
end

local function part2(moves)
  local santa = Pos{x = 0, y = 0}
  local robo = Pos{x = 0, y = 0}
  local santas_turn = true
  local visited = set()

  rset.add(visited, hash(santa))
  for _, dir in ipairs(moves) do
    if santas_turn then
      santa = move(santa, dir)
      rset.add(visited, hash(santa))
    else
      robo = move(robo, dir)
      rset.add(visited, hash(robo))
    end
    santas_turn = not santas_turn
  end
  return #visited
end

print(part1(load_moves('input.txt')))
print(part2(load_moves('input.txt')))

