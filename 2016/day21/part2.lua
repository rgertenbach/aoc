package.path = "/home/robin/src/llib/lua/?.lua;../lua/?.lua;" .. package.path
local f = assert(io.open("input.txt"))

local str = require("str")
local tbl = require("tbl")

---@enum Opcode
local Opcode = {
  SWP_POS = "SWP_POS", -- Position based swap.
  SWP_LET = "SWP_LET", -- Letter swap (translate).
  ROT_LOR = "ROT_LOR", -- Rotate entire string.
  ROT_POS = "ROT_POS", -- Rotate based on index of letter x.
  REV_POS = "REV_POS", -- Reverse positions X through Y.
  MOV_POS = "MOV_POS", -- Remove letter at position X and insert so it's at position Y.
}

---@enum
local Direction = {
  LEFT = "left",
  RIGHT = "right",
}

---@class Operation
---@field op Opcode
---@field x integer|string?
---@field y integer|string?
---@field d Direction?

---Create an operation
---@param op Opcode
---@param x integer|string?
---@param y integer|string?
---@parma d Direction
---@return Operation
local function make_operation(op, x, y, d)
  return {op=op, x=x, y=y, d=d}
end

local instructions = {}  ---@type Operation[]

for line in f:lines() do
  local x, y, direction
  x, y = line:match("^swap position (%d+) with position (%d+)$")
  if x then
    table.insert(instructions, make_operation(Opcode.SWP_POS, tonumber(x) + 1, tonumber(y) + 1))
    goto continue
  end

  x, y = line:match("^swap letter (%w) with letter (%w)$")
  if x then
    table.insert(instructions, make_operation(Opcode.SWP_LET, x, y))
    goto continue
  end

  direction, x = line:match("^rotate (%w+) (%d+) steps?$")
  if x then
    table.insert(instructions, make_operation(Opcode.ROT_LOR, tonumber(x), nil, direction))
    goto continue
  end

  x = line:match("^rotate based on position of letter (%w)$")
  if x then
    table.insert(instructions, make_operation(Opcode.ROT_POS, x))
    goto continue
  end

  x, y = line:match("^reverse positions (%d+) through (%d+)$")
  if x then
    table.insert(instructions, make_operation(Opcode.REV_POS, tonumber(x) + 1, tonumber(y) + 1))
    goto continue
  end

  x, y = line:match("^move position (%d+) to position (%d+)$")
  if x then
    table.insert(instructions, make_operation(Opcode.MOV_POS, tonumber(x) + 1, tonumber(y) + 1))
    goto continue
  end
  ::continue::
end

---@param s string[]
---@param op Operation
local function apply(s, op)
  if op.op == Opcode.SWP_POS then
    s[op.x], s[op.y] = s[op.y], s[op.x]

  elseif op.op == Opcode.SWP_LET then
    for i, c in ipairs(s) do
      if c == op.x then s[i] = op.y
      elseif c == op.y then s[i] = op.x
      end
    end

  elseif op.op == Opcode.ROT_LOR then
    local new = {}
    if op.d == Direction.RIGHT then
      for i = 1, #s do new[(i + op.x - 1) % #s + 1] = s[i] end
    else
      for i = 1, #s do new[(i + #s - op.x - 1) % #s + 1] = s[i] end
    end
    for i = 1, #s do s[i] = new[i] end

  elseif op.op == Opcode.ROT_POS then
    local pos = nil
    for i, c in ipairs(s) do
      if c == op.x then
        pos = i
        break
      end
    end
    pos = pos + (pos >= 5 and 1 or 0)
    local new = {}
    for i = 1, #s do
      new[(i + pos - 1)% #s + 1] = s[i]
    end
    for i = 1, #s do s[i] = new[i] end

  elseif op.op == Opcode.REV_POS then
    local l, r = op.x, op.y
    while l < r do
      s[l], s[r] = s[r], s[l]
      l = l + 1
      r = r - 1
    end

  elseif op.op == Opcode.MOV_POS then
    local c = s[op.x]
    if op.x < op.y then
      for i = op.x, op.y - 1 do
        s[i] = s[i+1]
      end
      s[op.y] = c
    else
      for i = op.x, op.y + 1, -1 do
        s[i] = s[i-1]
      end
      s[op.y] = c
    end

  else error("unknown op")
  end
end

local original = "abcdefgh"
local s = str.split(original, "")
for _, op in ipairs(instructions) do
  apply(s, op)
end
local original_indices = {}
for c in tbl.ivalues(s) do
  local i = string.find(original, c)
  table.insert(original_indices, i)
end
print(table.concat(original_indices))
local final = {}
for i in tbl.ivalues(original_indices) do
  table.insert(final, string.sub("fbgdceah", i, i))
end
print(table.concat(final))

local pos_shift_starts = {
  [2] = 1,
  [4] = 2,
  [6] = 3,
  [8] = 4,
  [3] = 5,
  [5] = 6,
  [7] = 7,
  [1] = 8
}

local function reverse_instruction(op)
  if op.op == Opcode.SWP_POS then return op end
  if op.op == Opcode.SWP_LET then return op end
  if op.op == Opcode.REV_POS then return op end
  if op.op == Opcode.MOV_POS then return make_operation(op.op, op.y, op.x) end
  if op.op == Opcode.ROT_LOR then
    local d = (op.d == Direction.RIGHT) and Direction.LEFT or Direction.RIGHT
    return make_operation(op.op, op.x, op.y, d)
  end
  if op.op == Opcode.ROT_POS then
    local end_pos = 0
    for j, c in ipairs(s) do
      if c == op.x then
        end_pos = j
        break
      end
    end
    assert(end_pos > 0)
    local start_pos = pos_shift_starts[end_pos]
    local lshift = (end_pos - start_pos + #s - 1) %#s + 1
    return make_operation(Opcode.ROT_LOR, lshift, nil, Direction.LEFT)
  end

  error(string.format("Unsupported Op %s", op.op))
end

local part2 = "fbgdceah"
s = str.split(part2, "")

for i = #instructions, 1, -1 do
  apply(s, reverse_instruction(instructions[i]))
end

print(table.concat(s))

