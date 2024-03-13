package.path = "../utils/?.lua;" .. package.path

local su = require("string_utils")

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
    print(input.room, input.sector_id)
    local checksum = calc_checksum(input.room)
    if checksum == input.checksum then
      real = real + input.sector_id
    end
  end
  io.stdout:write(real, "\n")
  file:close()
end
