local f = assert(io.open("input.txt"))


local state = {a=7, b=0, c=0, d=0}
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
  local op, x, y = table.unpack(instructions[p])
  -- print(string.format(
  --   "%d. %s: %s %s\ta:%d b:%d c:%d d:%d",
  --   p, op, x, y, state.a, state.b, state.c, state.d)
  -- )

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
    -- print("changing ", x)
    if x <= #instructions and x >= 1 then
      if     instructions[x][1] == "inc" then instructions[x][1] = "dec"
      elseif instructions[x][3] == nil   then instructions[x][1] = "inc"
      elseif instructions[x][1] == "jnz" then instructions[x][1] = "cpy"
      else                                    instructions[x][1] = "jnz"
      end
    end
    -- print(instructions[x][1])
  end
  p = p + 1
  -- print(string.format(
  --   "\tState is now p: %d a:%d b:%d c:%d d:%d",
  --   p, state.a, state.b, state.c, state.d)
  -- )
  -- if state.a > 20 then break end
end

print(state["a"])
