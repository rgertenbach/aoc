package.path = "../utils/?.lua;" .. package.path

for i = 1, #arg do
  io.stdout:write(arg[i], "\n")
  local file = assert(io.open(arg[i], "r"))
  local cnts = {}
  for line in file:lines() do
    for c = 1, #line do
      local char = line:sub(c, c)
      if cnts[c] == nil then cnts[c] = {}  end
      cnts[c][char] = (cnts[c][char] or 0) + 1
    end
  end
  local out = ""
  for i = 1, #cnts do
    local argmax
    for letter, freq in pairs(cnts[i]) do
      if argmax == nil or freq > cnts[i][argmax] then
        argmax = letter
      end
    end
    out = out .. argmax
 
  end
  print(out)

  file:close()
end
