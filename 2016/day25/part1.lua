local f = assert(io.open("input.txt"))



---@param p integer pointer
---@paran s table<string, integer> state
---@param o boolean isone
local function skey(p, s, o)
  return string.format("%d,%d,%d,%d,%d,%s", p, s.a, s.b, s.c, s.d, o)
end

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

local function attempt(init_a)
  local state = {a=init_a, b=0, c=0, d=633*4+init_a}
  local p = 9
  local last1 = true
  local done = {}
  done[skey(p, state, last1)] = true

  while p <= #instructions do
    local op, x, y = table.unpack(instructions[p])
    if op == "cpy" then state[y] = state[x] or tonumber(x) or 0
    elseif op == "inc" then state[x] = state[x] + 1
    elseif op == "dec" then state[x] = state[x] - 1
    elseif op == "jnz" then
      if tonumber(x) ~= nil then x = tonumber(x)
      else x = state[x] end
      if x ~= 0 then p = p + tonumber(y) - 1 end
    elseif op == "out" then
      if tonumber(x) ~= nil then x = tonumber(x)
      else x = state[x] end
      if last1 == (x == 1) then return false end
      last1 = not last1
    end
    p = p + 1
    if done[skey(p, state, last1)] then
      print("loop")
      return true
    end
    done[skey(p, state, last1)] = true
    -- print(skey(p, state, last1))
  end
end

local a = 1
while not attempt(a) do
  a = a + 1
end
print(a)
