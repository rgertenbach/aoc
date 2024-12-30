---@param line string
local function lengths(line)
  local chars = 2
  local i = 1
  while i <= #line do
    local c = line:sub(i, i)
    if c == "\"" or c == "\\" then chars = chars + 1
    end
    chars = chars + 1
    i = i + 1
  end
  return #line, chars
end

local f = assert(io.open("input.txt"))

local string_chars, memory_chars = 0, 0
for line in f:lines() do
  local s, m = lengths(line)
  string_chars = string_chars + s
  memory_chars = memory_chars + m
end
f:close()

print(memory_chars - string_chars)

