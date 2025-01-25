package.path = "/home/robin/src/llib/lua/?.lua;" .. package.path
local str = require("str")
local tbl = require("tbl")

local f = assert(io.open("input.txt"))

local warehouse = {}

local function copy_warehouse(wh)
  local out = {}
  for items in tbl.ivalues(wh) do
    local floor = {}
    for item in tbl.ivalues(items) do table.insert(floor, item) end
    table.insert(out, floor)
  end
  return out
end

local function is_legit(wh)
  for floor in tbl.ivalues(wh) do
    local generators = {}
    local has_generators = false
    for item in tbl.ivalues(floor) do
      local element, kind = item:sub(1, 1), item:sub(2, 2)
      if kind == "g" then
        generators[element] = true
        has_generators = true
      end
    end
    for item in tbl.ivalues(floor) do
      local element, kind = item:sub(1, 1), item:sub(2, 2)
      if kind == "m" and has_generators and not generators[element] then
        return false
      end
    end
  end
  return true
end

for line in f:lines() do
  table.insert(warehouse, {})
  line = line:gsub("The [^ ]+ floor contains ", "")
  if line ~= "nothing relevant." then
    for item in tbl.ivalues(str.split(line, ", ")) do
      local element, kind = item:match("a (%w)[^ ]+ (%w)")
      table.insert(warehouse[#warehouse], element .. kind)
    end
  end
end

f:close()

local function statekey(e, state)
  local out = {e .. "e"}
  for floor, items in ipairs(state) do
    table.sort(items)
    for item in tbl.ivalues(items) do
      table.insert(out, floor .. item)
    end

  end
  return table.concat(out)
end

local done = {}
done[statekey(1, warehouse)] = true
local steps = 0
local current = {{1, warehouse}}

while #current > 0 do
  -- print("Steps: ", steps)
  local nxt = {}
  for state in tbl.ivalues(current) do
    -- print("  State:", statekey(table.unpack(state)))
    local e, wh = table.unpack(state)
    if  #wh[1] == 0 and #wh[2] == 0 and #wh[3] == 0 then
      print(statekey(e, wh))
      print(steps)
      os.exit()
    end

    -- One item
    for i, item in ipairs(wh[e]) do
      if e > 1 then
        local pwh = copy_warehouse(wh)
        local pe = e - 1
        table.remove(pwh[e], i)
        table.insert(pwh[pe], item)
        local sk = statekey(pe, pwh)
        if not done[sk] and is_legit(pwh) then
          table.insert(nxt, {pe, pwh})
          done[sk] = true
        end
      end
      if e < 4 then
        local pwh = copy_warehouse(wh)
        local pe = e + 1
        table.remove(pwh[e], i)
        table.insert(pwh[pe], item)
        local sk = statekey(pe, pwh)
        if not done[sk] and is_legit(pwh) then
          table.insert(nxt, {pe, pwh})
          done[sk] = true
        end
      end
    end
    -- Two items
    for i, item in ipairs(wh[e]) do
      for i2, item2 in ipairs(wh[e]) do
        if i == i2 then goto continue end
        if e > 1 then
          local pwh = copy_warehouse(wh)
          local pe = e - 1
          table.remove(pwh[e], i)
          table.remove(pwh[e], i2)
          table.insert(pwh[pe], item)
          table.insert(pwh[pe], item2)
          local sk = statekey(pe, pwh)
          if not done[sk] and is_legit(pwh) then
            table.insert(nxt, {pe, pwh})
            done[sk] = true
          end
        end  -- Go down
        if e < 4 then
          local pwh = copy_warehouse(wh)
          local pe = e + 1
          table.remove(pwh[e], i)
          table.remove(pwh[e], i2)
          table.insert(pwh[pe], item)
          table.insert(pwh[pe], item2)
          local sk = statekey(pe, pwh)
          if not done[sk] and is_legit(pwh) then
            table.insert(nxt, {pe, pwh})
            done[sk] = true
          end
        end  -- Go up
      end  -- Item 2
      ::continue::
    end  -- Item 2
  end  -- State
  current = nxt
  steps = steps + 1
end



print(statekey(1, warehouse))
