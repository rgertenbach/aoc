package.path = "../utils/?.lua;" .. package.path
local collections = require("collections")
local robots = require("robots")

START_VALUE_PAT = "^value (%d+) goes to (bot %d+)$"
RULE_PAT = "^(bot %d+) gives low to (%w+ %d+) and high to (%w+ %d+)"

for i = 1, #arg do
  io.stdout:write(arg[i], "\n")
  local file = assert(io.open(arg[i], "r"))

  local bots = collections.defaultdict(robots.Bot.new, true)

  for line in file:lines() do
    if line:sub(1, 5) == "value" then
      local chip, bot = line:match(START_VALUE_PAT)
      bots[bot]:add_chip(tonumber(chip))
    else
      local bot, lowdest, highdest = line:match(RULE_PAT)
      bots[bot]:add_rule(lowdest, highdest)
    end
  end
  file:close()

  local o0, o1, o2 = nil, nil, nil
  while not (o0 and o1 and o2) do
    for name, bot in pairs(bots) do
      if bot:has_both(61, 17) then io.stdout:write("Part 1: ", name, "\n") end -- Both check
      if bot:is_bot() then bot:execute_rule(bots) end
      if bot.name == "output 0" and bot.chips.n > 0 then o0 = bot:get_chips() end
      if bot.name == "output 1" and bot.chips.n > 0 then o1 = bot:get_chips() end
      if bot.name == "output 2" and bot.chips.n > 0 then o2 = bot:get_chips() end
    end  -- each bot
  end

  io.stdout:write("Part 2: ", o0 * o1 * o2, "\n")

end
