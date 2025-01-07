WIDTH = 50
HEIGHT = 6


--- Turns on a w by h rectangle starting top left
--- @param t table the table to operate on
--- @param w integer Number of columns
--- @param h integer Number of rows
local function rect(t, w, h)
  for row = 1, h do
    for col = 1, w do
      t[row][col] = true
    end
  end
end

--- Right shifts pixels
--- @param t table The table to operate on.
--- @param r integer The row to shift
--- @param by integer How many positions to shift
local function rotate_row(t, r, by)
  local row = t[r]
  local newrow = {}
  for col, val in pairs(row) do
    newrow[(col + by - 1) % WIDTH + 1] = val
  end
  t[r] = newrow
end

--- Right shifts pixels
--- @param t table The table to operate on.
--- @param c integer The columns to shift
--- @param by integer How many positions to shift
local function rotate_col(t, c, by)
  local new = {}
  for row = 1, HEIGHT do new[(row + by - 1) % HEIGHT + 1] = t[row][c] end
  for row = 1, HEIGHT do t[row][c] = new[row] end
end

local function count_on(t)
  local cnt = 0
  for row = 1, HEIGHT do
    for col = 1, WIDTH do
      if t[row][col] then cnt = cnt + 1 end
    end
  end
  return cnt
end

local function print_t(t)
  for row = 1, HEIGHT do
    for col = 1, WIDTH do
      io.stdout:write(t[row][col] and '#' or ' ')
    end
    io.stdout:write('\n')

  end
end

local function parse(line, t)
  if line:sub(1, 4) == "rect" then
    local w, h = line:match("rect (%d+)x(%d+)")
    rect(t, math.tointeger(w), math.tointeger(h))
  elseif line:match("rotate row") then
    local row, by = line:match("y=(%d+) by (%d+)")
    rotate_row(t, math.tointeger(row) + 1, math.tointeger(by))
  elseif line:match("rotate column") then
    local col, by = line:match("x=(%d+) by (%d+)")
    rotate_col(t, math.tointeger(col) + 1, math.tointeger(by))
  end
end

for i = 1, #arg do
  io.stdout:write(arg[i], "\n")
  local file = assert(io.open(arg[i], "r"))
    local t = {{}, {}, {}, {}, {}, {}}
    for line in file:lines() do
      io.stdout:write(line, "\n")
      parse(line, t)
      print_t(t)
      print()
    end
    io.stdout:write(count_on(t), "\n")
  file:close()
end
