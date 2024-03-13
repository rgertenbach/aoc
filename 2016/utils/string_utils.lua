-- Not UTF-8 safe.
local function split_empty(s)
  local out = {}
  for i = 1, #s do
    table.insert(out, s:sub(i, i))
  end
  return out
end

local m = {}

function m.split(s, sep)
  local out = {}
  local word_start = 1
  if sep == "" then return split_empty(s) end
  while true do
    local sep_start, sep_end = s:find(sep, word_start)
    if sep_start == nil then break end
    table.insert(out, s:sub(word_start, sep_start - 1))
    word_start = sep_end + 1
  end
    table.insert(out, s:sub(word_start, #s))
  return out
end

return m

