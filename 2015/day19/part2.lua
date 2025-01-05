package.path = "/home/robin/src/llib/lua/?.lua;" .. package.path
local f = assert(io.open("input.txt"))
local lines = {}
for line in f:lines() do
  table.insert(lines, line)
end
f:close()

local molecule = table.remove(lines, #lines)
table.remove(lines, #lines)  -- Empty

local replacements = {}
local revrepl = {}
for _, line in ipairs(lines) do
  local part, replacement = line:match("^(%w+) => (%w+)$")
  if replacements[part] == nil then replacements[part] = {} end
  if revrepl[replacement] == nil then revrepl[replacement] = part else error("duplicate") end
  table.insert(replacements[part], replacement)
end

local steps = 0

local done = {done = true}
local h = {molecule}

local revrepls = {}
for tgt, src in pairs(revrepl) do
  table.insert(revrepls, {tgt=tgt, src=src})
end

-- Assumption: It's always better to use a longer replacement.
table.sort(revrepls, function(a, b) return #b.tgt < #a.tgt end)


while true do
  print(steps, #h)
  local new = {}
  for _, current in ipairs(h) do
    if current == "e" then
      print(steps)
      os.exit()
    end

    for _, r in ipairs(revrepls) do
      local tgt, src = r.tgt, r.src
      for i = 1, #current - #tgt + 1 do
        if current:sub(i, i + #tgt - 1) == tgt then
          local prop = current:sub(1, i-1) .. src .. current:sub(i + #tgt)
          if done[prop] == nil then
            done[prop] = true
            table.insert(new, prop)
            goto cont
          end
        end
      end
    end  -- replacements
  end
  ::cont::
  h = new
  steps = steps + 1
end
