package.path = "/home/robin/src/llib/lua/?.lua;" .. package.path

local tbl = require("tbl")

local f = assert(io.open("input.txt"))

---@param t number[]
---@return number
local function tmax(t)
  local mx = -math.huge
  for x in tbl.ivalues(t) do mx = math.max(mx, x) end
  return mx
end

_ = f:read("l")
_ = f:read("l")

local cap = {}  ---@type integer[][]
local use = {}  ---@type integer[][]
local rows = 0
local cols = 0

---@param used integer[][]
---@param capacity integer[][]
---@return string
local function format_grid(used, capacity)
  local maxes = {}
  for c in tbl.ivalues(capacity) do
    table.insert(maxes, tmax(c))
  end
  local max_cap = tmax(maxes)
  local max_cap_digits = #tostring(max_cap)
  local fstring = string.format("%%%dd/%%-%dd", max_cap_digits, max_cap_digits)
  local out_lines = {}
  for i, used_line in ipairs(used) do
    local cap_line = capacity[i]
    local out_line = {}
    for k, u in ipairs(used_line) do
      local c = cap_line[k]
      table.insert(out_line, string.format(fstring, u, c))
    end
    table.insert(out_lines, table.concat(out_line, " "))
  end

  return table.concat(out_lines, "\n")
end

for line in f:lines() do
  local x, y, c, u = line:match("^.*x(%d+)%-y(%d+) *(%d+)T *(%d+).*")
  x, y = assert(tonumber(x)) + 1, assert(tonumber(y)) + 1
  c, u = assert(tonumber(c)), assert(tonumber(u))
  if y > #cap then
    cap[y] = {}
    use[y] = {}
  end
  cap[y][x] = c
  use[y][x] = u
  rows = math.max(rows, y)
  cols = math.max(cols, x)
end
print(rows, cols)

print(format_grid(use, cap))
 

-- Visual inspection shows that all cells fit into the spare one except for the
-- big ones.
-- I can assume the big ones are immovable and all others are booleans (filled or empty)
-- That will allow me to memoize.
-- I can memoize more efficiently with bitmasks
