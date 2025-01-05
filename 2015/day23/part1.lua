local f = assert(io.open("input.txt"))

---@class Instruction
---@field op string
---@field r string register
---@field offset integer?

local instructions = {}  ---@type Instruction[]

for line in f:lines() do
  local op, p1, p2 = line:match("^(%w+) ([^ ,]+)(.*)$")
  local register, offset
  if op == "jmp" then
    offset = tonumber(p1)
  elseif #p2 > 0 then
    register = p1
    offset = tonumber(p2:match(", (.*)"))
  else
    register = p1
    offset = nil
  end
  table.insert(instructions, {op=op, r=register, offset=offset})
end

local a, b, p = 0, 0, 1

while p <= #instructions do
  local op, r, off = instructions[p].op, instructions[p].r, instructions[p].offset

  if op == "hlf" then
    if r == "a" then a = a // 2 else b = b // 2 end
    p = p + 1
  elseif op == "tpl" then
    if r == "a" then a = a * 3 else b = b * 3 end
    p = p + 1
  elseif op == "inc" then
    if r == "a" then a = a + 1 else b = b + 1 end
    p = p + 1
  elseif op == "jmp" then
    p = p + off
  elseif op == "jie" then
    if r == "a" and a % 2 == 0 then p = p + off
    elseif r == "b" and b % 2 == 0 then p = p + off
    else p = p + 1
    end
  elseif op == "jio" then
    if r == "a" and a == 1 then p = p + off
    elseif r == "b" and b == 1 then p = p + off
    else p = p + 1
    end
  else break
  end
end

print(a, b)
