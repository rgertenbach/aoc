local f = assert(io.open("input.txt"))


local state = {a=12, b=0, c=0, d=0}
local p = 1

local instructions = {}
for line in f:lines() do
  local op, x = line:match("^(%w+) (.*)")
  local y
  if op == "cpy" or op == "jnz" then
    x, y = x:match("^([^ ]+) ([^ ]+)")
  end
  table.insert(instructions, {op, x, y})
end
f:close()

while p <= #instructions do
  local op, x, y = unpack(instructions[p])

  if op == "cpy" then
    if tonumber(y) == nil then  -- Must be a valid register
      state[y] = state[x] or tonumber(x) or 0
    end
  elseif op == "inc" then
      state[x] = state[x] + 1
  elseif op == "dec" then
      state[x] = state[x] - 1
  elseif op == "jnz" then
    x = tonumber(x) or state[x] or 0
    y = tonumber(y) or state[y] or 0
    if x ~= 0 then
      p = p + tonumber(y) - 1
    end
  elseif op == "tgl" then
    x = p + state[x]
    if x <= #instructions and x >= 1 then
      if     instructions[x][1] == "inc" then instructions[x][1] = "dec"
      elseif instructions[x][3] == nil   then instructions[x][1] = "inc"
      elseif instructions[x][1] == "jnz" then instructions[x][1] = "cpy"
      else                                    instructions[x][1] = "jnz"
      end
    end
  end
  p = p + 1
end

print(state["a"])
