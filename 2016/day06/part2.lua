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
  local p1out = ""
  local p2out = ""
  for k = 1, #cnts do
    local argmax
    local argmin
    for letter, freq in pairs(cnts[k]) do
      if argmax == nil or freq > cnts[k][argmax] then argmax = letter
      elseif argmin == nil or freq < cnts[k][argmin] then argmin = letter end
    end
    p1out = p1out .. argmax
    p2out = p2out .. argmin

  end
  print(p1out)
  print(p2out)

  file:close()
end
