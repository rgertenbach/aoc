local function rotate(orientation, rotation)
  if orientation == 'N' then
    return rotation == 'R' and 'E' or 'W'
  elseif orientation == 'E' then
    return rotation == 'R' and 'S' or 'N'
  elseif orientation == 'S' then
    return rotation == 'R' and 'W' or 'E'
  elseif orientation == 'W' then
    return rotation == 'R' and 'N' or 'S'
  end
end


local function move(x, y, orientation, steps)
  if orientation == "N" then return x, y + steps
  elseif orientation == "S" then return x, y - steps
  elseif orientation == "W" then return x - steps, y
  elseif orientation == "E" then return x + steps, y
  end
end

local function follow_instruction(instruction, x, y, orientation)
  local rotation = string.sub(instruction, 1, 1)
  local steps = tonumber(string.sub(instruction, 2))
  orientation = rotate(orientation, rotation)
  x, y = move(x, y, orientation, steps)

  return x, y, orientation
end

local function split(instructions)
  return string.gmatch(instructions, "%a%d+")
end

local function follow_tape(instructions, x, y, orientation)
  for instruction in split(instructions) do
    x, y, orientation = follow_instruction(instruction, x, y, orientation)
  end
  return x, y, orientation
end

local function main()
  local file = io.open("input.txt")
  if file == nil then
    return
  end
  local instructions = file:read("l")
  local x, y = follow_tape(instructions, 0, 0, "N")
  x = math.abs(x)
  y = math.abs(y)
  print(x + y)
  file:close()
end

main()
