package.path = "/home/robin/src/llib/lua/?.lua;" .. package.path

local tbl = require("tbl")

local f = assert(io.open("input.txt"))

_ = f:read("l")
_ = f:read("l")

local rows = 0
local cols = 0

local function key(row, col)
  return string.format("%d,%d", row, col)
end

local function make_state(free_row, free_col, target_row, target_col)
  return key(free_row, free_col) .. "," .. key(target_row, target_col)
end

local frow, fcol = 0, 0

local immovable = {}  ---@type table<string, boolean>

for line in f:lines() do
  local x, y, c, u = line:match("^.*x(%d+)%-y(%d+) *(%d+)T *(%d+).*")
  local col, row = assert(tonumber(x)) + 1, assert(tonumber(y)) + 1
  c, u = assert(tonumber(c)), assert(tonumber(u))
  if u == 0 then
    frow = row
    fcol = col
  elseif u > 100 then
    immovable[key(row, col)] = true
  end
  rows = math.max(rows, row)
  cols = math.max(cols, col)
end

local trow = 1
local tcol = cols
local states_explored = {}  ---@type table<string, boolean>
states_explored[make_state(frow, fcol, trow, tcol)] = true

local frontier = {{frow, fcol, trow, tcol}}
local steps = 0

while #frontier > 0 do
  local next_frontier = {}
  for state in tbl.ivalues(frontier) do
    frow, fcol, trow, tcol = table.unpack(state)
    if trow == 1 and tcol == 1 then
      print(steps)
      os.exit()
    end
    for prop in tbl.ivalues({{frow - 1, fcol}, {frow + 1, fcol}, {frow, fcol - 1}, {frow, fcol + 1}}) do
      local pfrow, pfcol = table.unpack(prop)
      if (
        pfrow == 0 or pfrow > rows or
        pfcol == 0 or pfcol > cols or
        immovable[key(pfrow, pfcol)]
      ) then goto continue end
      local ptrow, ptcol
      if pfrow == trow and pfcol == tcol then ptrow, ptcol = frow, fcol
      else ptrow, ptcol = trow, tcol
      end
      local st = make_state(pfrow, pfcol, ptrow, ptcol)
      if states_explored[st] then goto continue end
      states_explored[st] = true
      table.insert(next_frontier, {pfrow, pfcol, ptrow, ptcol})
      ::continue::
    end
  end
  frontier = next_frontier
  steps = steps + 1
end
