---@param pw string
---@return boolean
local function isgood(pw)
  local three = false
  local last_pair_start = -10
  local npairs = 0
  for i = 1, #pw do
    local c = pw:sub(i, i)
    if c == "i" or c == "o" or c == "l" then return false end
    if i >= 2 and pw:sub(i-1, i-1) == c and i - last_pair_start >= 2 then
      npairs = npairs + 1
      last_pair_start = i
    end
    if (
      i >= 3
      and string.byte(c) - string.byte(pw:sub(i-1, i-1)) == 1
      and string.byte(c) - string.byte(pw:sub(i-2, i-2)) == 2)
     then three = true
     end
   end
  return three and npairs >= 2
end

ZORD = string.byte("z")
AORD = string.byte("a")
IORD = string.byte("i")
OORD = string.byte("o")
LORD = string.byte("l")

---@param pw string
---@return string
local function inc(pw)
  local rev = {}
  local carry = 0
  for i = #pw, 1, -1 do
    local cord = string.byte(pw:sub(i, i)) + carry
    if i == #pw then cord = cord + 1 end
    if cord == IORD or cord == OORD or cord == LORD then
      local new_rev = {}
      for _ = 1, #rev do table.insert(new_rev, "a") end
      rev = new_rev
      cord = cord + 1
    end
    carry = cord > ZORD and 1 or 0
    cord = AORD + (cord - AORD) % 26
    table.insert(rev, string.char(cord))
  end
  return string.reverse(table.concat(rev))
end

local function nextpw(pw)
  pw = inc(pw)
  while not isgood(pw) do
    pw = inc(pw)
  -- print(pw)
  end
  return pw
end

local pw = "hepxcrrq"
pw = nextpw(pw)
print("part 1", pw)
pw = nextpw(pw)
print("part 2", pw)



