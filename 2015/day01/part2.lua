#!/usr/bin/lua
floor = 0
moves = arg[1]
for i = 1, #moves do
  if moves:sub(i, i) == '(' then floor = floor + 1 else floor = floor - 1 end
  if floor < 0 then 
    print(i)
    break 
  end
end
