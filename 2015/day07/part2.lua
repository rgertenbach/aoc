local MASK16 = 65535

---@alias InputKind "LITERAL" | "VARIABLE"

---@alias Operation "REFERENCE" | "NOT" | "AND" | "OR" | "LSHIFT" | "RSHIFT"

---@class Input
---@field kind InputKind
---@field value number | string

---@class Gate
---@field target string
---@field op Operation
---@field a Input
---@field b Input | nil


---@param input string
---@return Input
local function parse_input(input)
  if tonumber(input) ~= nil then
    return {kind = "LITERAL", value = tonumber(input)}
  end
  return {kind = "VARIABLE", value = input}
end

---@param input Input
---@return string
local function finput(input)
  if input == nil then return "" end
  if input.kind == "LITERAL" then return string.format("LIT %d", input.value) end
  return string.format("REF %s", input.value)
end

---@param line string
---@return Gate
local function parse_line(line)
  local out = {}
  local left
  left, out.target = line:match("^(.*) %-> (.*)$")
  -- This only really handles the single last key step
  if not left:find(" ") then
    out.a = parse_input(left)
    out.op = "REFERENCE"
    return out
  end

  local a = left:match("^NOT (%w+)$")
  if a then
    out.op = "NOT"
    out.a = parse_input(a)
    return out
  end
  local op, b
  a, op, b = left:match("^(%w+) (%w+) (%w+)$")
  out.a = parse_input(a)
  out.b = parse_input(b)
  out.op = op

  return out
end

---@param gate Gate
---@return string
local function fgate(gate)
  local a = finput(gate.a)
  local b = finput(gate.b)
  return string.format("%s: %s of (%s) and (%s)", gate.target, gate.op, a, b)
end

local f = assert(io.open("input.txt"))
---@type table<string, Gate>
local wiring = {}
for line in f:lines() do
  local gate = parse_line(line)
  wiring[gate.target] = gate
end
f:close()

---@type table<string, number>
local state = {}

---@param x string
---@return number
local function get_state(x)
  local function eval_variable(variable)
    if variable.kind == "LITERAL" then return variable.value end
    return get_state(variable.value)
  end

  if state[x] then return state[x] end
  local gate = wiring[x]
  -- print(fgate(gate))
  local a = eval_variable(gate.a)

  if gate.op == "REFERENCE" then state[x] = a
  elseif gate.op == "NOT" then state[x] = ~a & MASK16
  end
  if state[x] then return state[x] end

  local b = eval_variable(gate.b)
  if gate.op == "AND" then state[x] = a & b
  elseif gate.op == "OR" then state[x] = a | b
  elseif gate.op == "LSHIFT" then state[x] = a << b & MASK16
  elseif gate.op == "RSHIFT" then state[x] = a >> b
  end
  -- print(string.format("  %s", state[x]))
  return state[x]
end

local a = get_state("a")
state = {}
wiring.b = {
  target = "b",
  op = "REFERENCE",
  a = {kind = "LITERAL", value = a}
}
print(get_state("a"))

