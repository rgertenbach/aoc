local f = assert(io.open("input.txt"))


local state = {a=0, b=0, c=0, d=0}
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
  if op == "cpy" then state[y] = state[x] or tonumber(x) or 0
  elseif op == "inc" then state[x] = state[x] + 1
  elseif op == "dec" then state[x] = state[x] - 1
  elseif op == "jnz" then if state[x] ~= 0 then p = p + tonumber(y) - 1 end
  end
  p = p + 1
end

print(state["a"])
