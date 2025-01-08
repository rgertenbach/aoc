local f = assert(io.open("input.txt"))
local json = f:read("*l")
local parse_message, parse_array

---@param i integer
---@return boolean, integer Result it's red and where it ends.
local function parse_string(i)
  i = i + 1
  local last = i
  while json:sub(last, last) ~= "\"" do last = last + 1 end
  local isred = json:sub(i, last - 1) == "red"
  return isred, last
end

---@param i integer
---@return integer, integer Result The value and where it ends
local function parse_number(i)
  local isneg = false
  local val = 0
  if json:sub(i, i) == "-" then
    isneg = true
    i = i + 1
  end
  while tonumber(json:sub(i, i)) do
    val = val * 10
    val = val + tonumber(json:sub(i, i))
    i = i + 1
  end
  if isneg then val = -val end
  return val, i - 1
end

---@param i integer
---@return integer, integer Points and where it ends.
function parse_array(i)
  local total = 0
  local element_points = 0
  i = i + 1
  while json:sub(i, i) ~= "]" do
    if json:sub(i, i) == "[" then
      element_points, i = parse_array(i)
    elseif json:sub(i, i) == "{" then
      element_points, i = parse_message(i)
    elseif json:sub(i, i) == "\"" then
      _, i = parse_string(i)
    elseif json:sub(i, i) == "]" then
      break
    else
      element_points, i = parse_number(i)
    end
    total = total + element_points
    element_points = 0
    i = i + 1
    if json:sub(i, i) == "," then i = i + 1 end
  end
  return total, i
end

---@param i integer
---@return integer, integer Points and where it ends.
function parse_message(i)
  local isred = false
  local localred = false
  local total = 0
  local element_points = 0
  i = i + 1
  while json:sub(i, i) ~= "}" do
    _, i = parse_string(i)
    i = i + 2  -- past closing token and : 
    if json:sub(i, i) == "[" then element_points, i = parse_array(i)
    elseif json:sub(i, i) == "{" then element_points, i = parse_message(i)
    elseif json:sub(i, i) == "\"" then
      localred, i = parse_string(i)
      isred = isred or localred
    else
      element_points, i = parse_number(i)
    end
    total = total + element_points
    element_points = 0
    i = i + 1
    if json:sub(i, i) == "," then i = i + 1 end
  end
  if isred then total = 0 end
  return total, i
end



print(parse_array(1))
