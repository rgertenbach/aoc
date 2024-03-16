package.path = "/home/robin/lua/lib/?.lua;" .. package.path

local md5 = require "md5"
local rstring = require "rstring"

local function crack_hash(start, n_zeros)
  local i = 0
  local zeros = string.rep("0", n_zeros)
  while not rstring.starts_with(md5.sumhexa(start .. i), zeros) do
    if i % 1000 == 0 then print(i) end
    i = i + 1
  end
  return i
end


print(crack_hash("ckczppom", 5))
print(crack_hash("ckczppom", 6))
