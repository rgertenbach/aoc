package.path = "../utils/?.lua;" .. package.path

local su = require("string_utils")

local function shift(s, n)
  n = n % 26
  local a = string.byte("a")
  local out = ""
  for i = 1, #s do
    local c = s:sub(i, i)
    if c == '-' then out = out .. " "
    else
      out = out .. string.char((string.byte(c) - a + n) % 26 + a)
    end
  end
  return out
end

local function parse_input(s)

  local split = su.split(s, "%[")
  local checksum = split[2]:sub(1, #split[2] - 1)
  local sector_id = math.tointeger(split[1]:match("%d+"))
  local room = split[1]:match("[a-z-]+")
  room = room:sub(1, #room - 1)
  return {room = room, sector_id = sector_id, checksum = checksum}
end

local function calc_checksum(s)
  local freqs = {}
  s = s:gsub("-", "")
  s = s:gsub("%d", "")
  for i = 1, #s do
    if freqs[s:sub(i, i)] == nil then
      freqs[s:sub(i, i)] = 0
    end
    freqs[s:sub(i, i)] = freqs[s:sub(i, i)] + 1
  end

  local sfreqs = {}
  for k, v in pairs(freqs) do
    table.insert(sfreqs, {key=k, value=v})
  end
  table.sort(sfreqs, function(x, y)
    if x.value < y.value then return true end
    if x.value > y.value then return false end
    if x.key > y.key then return true end
    return false
  end)
  local chk = ""
  for i = 0, 4 do
    chk = chk .. sfreqs[#sfreqs - i].key
  end
  return chk
end



for i = 1, #arg do
  io.stdout:write(arg[i], "\n")
  local file = io.open(arg[i], "r")
  if file == nil then
    io.stderr:write("Failed to open ", arg[i], "\n")
    os.exit(1)
  end
  local real = 0
  while true do
    local line = file:read("*l")
    if line == nil then break end
    local input = parse_input(line)
    local checksum = calc_checksum(input.room)
    if checksum == input.checksum then
      real = real + input.sector_id
      local room_name = shift(input.room, input.sector_id)
      if room_name == "northpole object storage" then
        io.stdout:write("Part 2: ", input.sector_id, "\n")
      end
    end
  end
  io.stdout:write(real, "\n\n")
  file:close()
end
