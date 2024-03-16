#!/usr/bin/lua
floor = 0
for c in arg[1]:gmatch('.') do
  if c == '(' then floor = floor + 1 else floor = floor - 1 end
end
print(floor)
