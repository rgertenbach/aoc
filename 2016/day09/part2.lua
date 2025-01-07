local function parse(s, i)
  local last = i
  local nreps = 0
  local nchar
  i = i or 1
  if i > #s then return 0 end
  if s:sub(i, i) ~= "(" then return 1 + parse(s, i + 1) end

  -- How many characters to take
  nchar, last = s:match("(%d+)()", i + 1)
  nchar = math.tointeger(nchar)
  i = math.tointeger(last) + 1 -- account for x

  -- How many repetitions
  nreps, last = s:match("(%d+)()", i)
  nreps = math.tointeger(nreps)
  i = math.tointeger(last) + 1 -- account for )

  local rep_str = s:sub(i, i + nchar - 1)
  return nreps * parse(rep_str) + parse(s, i + nchar)

end

for i = 1, #arg do
  io.stdout:write(arg[i], "\n")
  local file = assert(io.open(arg[i], "r"))
  for line in file:lines() do
    io.stdout:write("Part 2: ", string.format("%d", parse(line)), "\n")
  end

  file:close()
end

-- 44866 is too low
