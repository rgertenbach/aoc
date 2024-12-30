---@param line string
local function lengths(line)
  local chars = 0
  local i = 1
  while i <= #line do
    if i == 1 or i == #line then chars = chars - 1
    elseif line:sub(i, i) == "\\" then
      if line:sub(i + 1, i + 1) == "\\" or line:sub(i + 1, i + 1) == "\""then i = i + 1
      elseif line:sub(i + 1, i + 1) == "x" then i = i + 3
      else error(string.format("Unexpected character at position %d of %s", i, line))
      end
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

print(string_chars - memory_chars)

