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

local function intersect(p1, p2)
  if p1[1] == p1[3] then  -- Vertical
    if p2[1] == p2[3] then -- Also vertical
      if p1[1] ~= p2[1] then return false end
      if p1[2] >= p2[2] and p1[2] <= p2[4] then return true end
      if p1[4] >= p2[2] and p1[4] <= p2[4] then return true end
      if p2[2] >= p1[2] and p2[2] <= p1[4] then return true end
      if p2[4] >= p1[2] and p2[4] <= p1[4] then return true end
      return false
    end
    -- Crossing
  end
  if p1[2] == p1[4] then  -- Horizontal
    if p2[2] == p2[4] then -- Also Horizontal
      if p1[2] ~= p2[2] then return false end

      if p1[1] >= p2[1] and p1[1] <= p2[4] then return true end
      if p1[3] >= p2[1] and p1[3] <= p2[4] then return true end
      if p2[1] >= p1[1] and p2[1] <= p1[4] then return true end
      if p2[3] >= p1[1] and p2[3] <= p1[4] then return true end
    end
  end
end

local function any_intersect(paths, path)
  for _, other in ipairs(paths) do
    local int_x, int_y = intersect(other, path)
    if int_x then return int_x, int_y end
  end
  return nil
end

local function follow_tape(instructions, x, y, orientation)
  local paths = {}
  for instruction in split(instructions) do
    local old_x, old_y = x, y
    x, y, orientation = follow_instruction(instruction, x, y, orientation)
    path  = {old_x, old_y, x, y}
    local int_x, int_y = any_intersect(paths, path)
    if int_x then return int_x, int_y end
    paths[#paths] = path
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
  print(x)
  file:close()
end

main()
