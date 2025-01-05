local f = assert(io.open("input.txt"))
local lines = {}
for line in f:lines() do
  table.insert(lines, line)
end
f:close()

local molecule = table.remove(lines, #lines)
table.remove(lines, #lines)  -- Empty

local replacements = {}
for _, line in ipairs(lines) do
  local part, replacement = line:match("^(%w+) => (%w+)$")
  if replacements[part] == nil then replacements[part] = {} end
  table.insert(replacements[part], replacement)
end

local mseq = {}
for x in molecule:gmatch("([A-Ze][a-z]?)") do
  table.insert(mseq, x)
end

local function copy(l)
  local out = {}
  for _, x in ipairs(l) do table.insert(out, x) end
  return out
end

local patterns = {}
for i, x in ipairs(mseq) do
  if replacements[x] ~= nil then
    for _, repl in ipairs(replacements[x]) do
      local new = copy(mseq)
      new[i] = repl
      patterns[table.concat(new)] = true
    end
  end
end

local total = 0
for _, _ in pairs(patterns) do total = total + 1 end
print(total)

