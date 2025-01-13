package.path = "../../../llib/lua/?.lua;" .. package.path

local dll = require("dlist")

local input = 3018458
local current = dll.node(1)
local first = current
while current.val < input do
  dll.insert_after(current, current.val + 1)
  current = current.next
end

current.next = first
first.prev = current
current = first

while current.next ~= current do
  dll.remove_next(current)
  current = current.next
end

print(current.val)
