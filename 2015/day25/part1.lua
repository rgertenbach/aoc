TARGET_ROW = 2947
TARGET_COL = 3029
MUL = 252533
MULB = "0000000111101101001110101"
MOD = 33554393
MODB = "1111111111111111111011001"

---@param x integer
---@return string
local function fbin(x)
  local out = {}
  while x > 0 do
    table.insert(out, x & 1)
    x = x >> 1
  end
  while #out < 25 do
    table.insert(out, 0)
  end

  return table.concat(out):reverse()
end

local paper = {
  {20151125, 18749137, 17289845, 30943339, 10071777, 33511524},
  {31916031, 21629792, 16929656, 7726640, 15514188, 4041754},
  {16080970, 8057251, 1601130, 7981243, 11661866, 16474243},
  {24592653, 32451966, 21345942, 9380097, 10600672, 31527494},
  {77061, 17552253, 28094349, 6899651, 9250759, 31663883},
  {33071741, 6796745, 25397450, 24659492, 1534922, 27995004},
}

for _, row in ipairs(paper) do
  for _, x in ipairs(row) do
    io.write(fbin(x), " ")
  end
  print()
end

local current = 20151125
local cr = 1
local cc = 1

while not (cr == TARGET_ROW and cc == TARGET_COL) do
  current = (current * MUL) % MOD
  if cr == 1 then
    cr = cc + 1
    cc = 1
  else
    cr = cr - 1
    cc = cc + 1
  end
end
print(current)
