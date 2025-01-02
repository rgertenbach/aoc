local f = assert(io.open("input.txt"))

local required = {
  children = 3,
  cats = 7,
  samoyeds = 2,
  pomeranians = 3,
  akitas = 0,
  vizslas = 0,
  goldfish = 5,
  trees = 3,
  cars = 2,
  perfumes = 1,
}

for line in f:lines() do
  local sue = tonumber(line:match("Sue (%d+)"))
  local children = tonumber(line:match("children: (%d+)"))
  local cats = tonumber(line:match("cats: (%d+)"))
  local samoyeds = tonumber(line:match("samoyeds: (%d+)"))
  local pomeranians = tonumber(line:match("pomeranians: (%d+)"))
  local akitas = tonumber(line:match("akitas: (%d+)"))
  local vizslas = tonumber(line:match("vizslas: (%d+)"))
  local goldfish = tonumber(line:match("goldfish: (%d+)"))
  local trees = tonumber(line:match("trees: (%d+)"))
  local cars = tonumber(line:match("cars: (%d+)"))
  local perfumes = tonumber(line:match("perfumes: (%d+)"))
  if (
    (children == nil or children == required.children) and
    (cats == nil or cats == required.cats) and
    (samoyeds == nil or samoyeds == required.samoyeds) and
    (pomeranians == nil or pomeranians == required.pomeranians) and
    (akitas == nil or akitas == required.akitas) and
    (vizslas == nil or vizslas == required.vizslas) and
    (goldfish == nil or goldfish == required.goldfish) and
    (trees == nil or trees == required.trees) and
    (cars == nil or cars == required.cars) and
    (perfumes == nil or perfumes == required.perfumes)) then
    print(sue)
  end
end
