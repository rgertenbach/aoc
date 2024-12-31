local current = "1113222113"

---@param input string
---@return string
local function rle(input)
  local cc = input:sub(1, 1)
  local cn = 1
  local out = {}
  for i = 2, #input do
    local c = input:sub(i, i)
    if c ~= cc then
      table.insert(out, cn .. cc)
      cc = c
      cn = 0
    end
    cn = cn + 1
  end
  table.insert(out, cn .. cc)
  return table.concat(out)
end

for _ = 1, 40 do current = rle(current) end
print(string.format("Part 1: %d", #current))
for _ = 1, 10 do current = rle(current) end
print(string.format("Part 1: %d", #current))
