local MASK16 = 65535

local function parse_input(input)
  if tonumber(input) ~= nil then
    return {kind = "LITERAL", value = tonumber(input)}
  end
  return {kind = "VARIABLE", value = input}
end

local function finput(input)
  if input == nil then return "" end
  if input.kind == "LITERAL" then return string.format("LIT %d", input.value) end
  return string.format("REF: %s", input.value)
end

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
  out.a, out.op, out.b = left:match("^(%w+) (%w+) (%w+)$")
  out.a = parse_input(out.a)
  out.b = parse_input(out.b)

  return out
end

local function fgate(gate)
  local a = finput(gate.a)
  local b = finput(gate.b)
  return string.format("%s: %s of (%s) and (%s)", gate.target, gate.op, a, b)
end

local f = assert(io.open("input.txt"))
local wiring = {}
for line in f:lines() do
  local gate = parse_line(line)
  wiring[gate.target] = gate
end
f:close()

local state = {}

local function get_state(x)
  local function eval_variable(variable)
    if variable.kind == "LITERAL" then return variable.value end
    return get_state(variable.value)
  end

  if state[x] then return state[x] end
  local gate = wiring[x]
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
  return state[x]

end

print(get_state("a"))

