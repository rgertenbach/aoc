package.path = "../utils/?.lua;" .. package.path

local function parse(s)
  local out = {}
  local i = 1
  while i <= #s do
    if s:sub(i, i) == "(" then
      local nchar, last = s:match("(%d+)()", i + 1)
      i = math.tointeger(last) + 1 -- account for x
      local nreps, last = s:match("(%d+)()", i)
      i = math.tointeger(last) + 1 -- account for )
      local rep_str = s:sub(i, i + math.tointeger(nchar) - 1)
      out[#out + 1] = string.rep(rep_str, math.tointeger(nreps))
      i = i + nchar

    else
      out[#out + 1] = s:sub(i, i)
      i = i + 1
    end
  end
  return table.concat(out)
end

for i = 1, #arg do
  io.stdout:write(arg[i], "\n")
  local file = assert(io.open(arg[i], "r"))
  for line in file:lines() do
    print(#parse(line))
  end
  
  file:close()
end

-- 44866 is too low
