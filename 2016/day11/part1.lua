package.path = "../utils/?.lua;" .. package.path

local wh = require("warehouse")

for i = 1, #arg do
  io.stdout:write(arg[i], "\n")
  local file = assert(io.open(arg[i], "r"))
  local floors = {}
  for line in file:lines() do
    table.insert(floors, wh.floor.Floor:parse(line))
  end
  local warehouse = wh.Warehouse:new(floors)
  print(warehouse:to_string())
  file:close()
end
