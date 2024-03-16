from typing import Iterable, Optional, Union
from collections import namedtuple, Counter
import re
import time 

CYCLES = 32
ORE = 'ore'
CLAY = 'clay'
OBS = 'obsidian'
GEODE = 'geode'

Resources = namedtuple('Resources', [ORE, CLAY, OBS, GEODE])
Blueprint = namedtuple('Blueprint', ['id', ORE, CLAY, OBS, GEODE])
Cache = dict[Union[str, tuple[Resources, Resources, int]], int]


def parse_costs(s: str) -> Resources:
  s = re.sub(r'Each \w+ robot costs ', '', s).strip('.')
  costs = s.split(' and ')
  costs = [cost.split(' ') for cost in costs]
  costs = {mat: int(amt) for amt, mat in costs}
  costs = [
          costs[ore] if ore in costs else 0 
          for ore in [ORE, CLAY, OBS, GEODE]]
  return Resources(*costs)


def parse_blueprint(bp: str) -> Blueprint:
    bpid, costs = bp.split(': ')
    bpid = int(bpid.lstrip('Blueprint '))
    costs = costs.split('. ')
    costs = [parse_costs(cost) for cost in costs]
    return Blueprint(bpid, *costs)


def load_data(filename) -> tuple[Blueprint, ...]:
    with open(filename) as f:
        blueprints = f.read().strip().split('\n')

    return tuple([parse_blueprint(bp) for bp in blueprints])


def make_res(ore: int = 0, 
             clay: int = 0, 
             obs: int = 0, 
             geode: int = 0, 
             old: Optional[Resources] = None) -> Resources:
  if old is None:
      return Resources(ore, clay, obs, geode)
  return Resources(ore + old.ore, clay + old.clay, obs + old.obsidian, geode + old.geode)


def add_res(a: Resources, b: Resources) -> Resources:
  return make_res(*a, b)


def mine(robots: Resources, old: Resources) -> Resources:
    return add_res(robots, old)


def can_afford(what: str, resources: Resources, bp: Blueprint) -> bool:
    cost = {ORE: bp.ore, CLAY: bp.clay, OBS: bp.obsidian, GEODE: bp.geode}[what]
    for need, have in zip(cost, resources):
        if need > have:
            return False
    return True


def build(what: str, 
          resources: Resources, 
          bp: Blueprint, 
          robots: Resources) -> tuple[Resources, Resources]:
    """Returns robots, resources"""
    cost = {ORE: bp.ore, CLAY: bp.clay, OBS: bp.obsidian, GEODE: bp.geode}[what]

    have_ore, have_clay, have_obs, have_geode = resources
    need_ore, need_clay, need_obs, need_geode = cost
    out_res = Resources(
            have_ore - need_ore, have_clay - need_clay, 
            have_obs - need_obs, have_geode - need_geode)
    out_rob = make_res(what == ORE, what == CLAY, what == OBS, what == GEODE, robots)
    return out_rob, out_res


def has_naive_resource_shortfall(resources, robots, bp, cycles):
    ore, clay, obs, geode = robots
    if geode:
        return False

    ore, clay, obs, geode = make_res(ore + cycles, clay + cycles, obs + cycles)
    resources = make_res(ore * cycles, clay * cycles, obs * cycles, 0, resources)

    return not can_afford(GEODE, resources, bp)

def has_naive_resource_shortfall2(resources, robots, bp, cycles, best):
    ore_miners, clay_miners, obs_miners, geode_miners = robots
    geode_trend = resources.geode + geode_miners * cycles
    if geode_trend > best:
      return False

    needed_to_be_better = best - geode_trend
    ore_cost, clay_cost, obs_cost, geode_cost = bp.geode

    # optimistic
    ore_trend = resources.ore + ore_miners * cycles + cumsum(cycles)
    clay_trend = resources.clay + clay_miners * cycles + cumsum(cycles)
    obs_trend = resources.obsidian + obs_miners * cycles + cumsum(cycles)

    many = 99999999999999999
    max_inc_geode_miners = min(
        ore_trend // ore_cost if ore_cost else many, 
        clay_trend // clay_cost if clay_cost else many, 
        obs_trend // obs_cost if obs_cost else many)
    max_inc_geodes = max_inc_geode_miners * cycles


    return geode_trend + max_inc_geodes <= best

def cumsum(n: int) -> int:
    return (n * (n + 1)) // 2

def naive_headroom(robots, current, remaining):
    return current + remaining * robots + cumsum(remaining)



def optimize_one_step(
        robots: Resources, 
        resources: Resources, 
        cycle: int, 
        blueprint: Blueprint,
        cache: Cache) -> int:
    if cycle >= CYCLES:
        cache['most_geodes'] = max(resources.geode, cache['most_geodes'])
        return resources.geode

    max_ore_need = max(blueprint.ore.ore, blueprint.clay.ore, blueprint.obsidian.ore,
            blueprint.geode.ore)
    max_clay_need = max(blueprint.clay.clay, blueprint.clay.clay, blueprint.obsidian.clay,
            blueprint.geode.clay)

    max_obsidian_need = max(blueprint.obsidian.obsidian, blueprint.clay.obsidian, blueprint.obsidian.obsidian,
            blueprint.geode.obsidian)

    # HEURISTIC PRUNING ########################################################

    # Skip last branch if we don't have a single geode yet as we won't get any
    # if cycle == CYCLES - 1 and not robots.geode:
    #     return 0

    # Penultimate pruning if we won't be able to build a geode robot next round.
    if cycle == CYCLES - 2 and not robots.geode and not can_afford(GEODE, mine(resources, robots),
            blueprint):
        return 0

    # Prune if we couldn't build a geode robot even if we got 3 of each 4 cycles
    # before the end.
    # if not robots.geode and has_naive_resource_shortfall(resources, robots, blueprint, CYCLES - cycle - 1):
    #     return 0

    # Prune if we couldn't build enough geode robot even if we got 3 of each 4
    # cycles before the end.
    if not robots.geode and has_naive_resource_shortfall2(resources, robots, blueprint, CYCLES - cycle - 1, cache['most_geodes']):
        return 0

    if naive_headroom(robots.geode, resources.geode, CYCLES - cycle) < cache['most_geodes']:
        return 0

    # END OF HEURISTIC PRUNING #################################################

    key = (robots, resources, cycle)
    if key in cache:
        return cache[key]

    # Wait
    best = optimize_one_step(
            robots, mine(robots, resources), cycle + 1, blueprint, cache)
    
    needed_res = [GEODE]
    if robots.ore < max_ore_need:
        needed_res.append(ORE)
    if robots.clay < max_clay_need:
        needed_res.append(CLAY)
    if robots.obsidian < max_obsidian_need:
        needed_res.append(OBS)
    # Try to build a mining robot
    for resource in needed_res:
        if can_afford(resource, resources, blueprint):
            a_rob, a_res = build(resource, resources, blueprint, robots)
            a_res = mine(robots, a_res)
            best = max(best, optimize_one_step(a_rob, a_res, cycle + 1, blueprint, cache))

    cache[key] = best
    return best


def optimize_blueprint(blueprint: Blueprint) -> int:
    robots = make_res(ore=1)
    resources = make_res()
    cache: Cache = {'most_geodes': 0}
    return optimize_one_step(robots, resources, 0, blueprint, cache)


def total_quality_levels(filename: str):
    print(filename)
    blueprints = load_data(filename)
    quality_levels = []
    start_time = time.time()
    for bp in blueprints[:3]:
        current_start_time = time.time()
        geodes = optimize_blueprint(bp)
        quality_level = bp.id * geodes
        quality_levels.append(quality_level)
        print(f'Finished Blueprint {bp.id}, took {time.time() - current_start_time:.0f} seconds')
    print(f'Finished, took {time.time() - start_time:.0f} seconds total')
    return sum(quality_levels)


def prod_geodes(filename: str):
    print(filename)
    blueprints = load_data(filename)
    geodes = []
    start_time = time.time()
    for bp in blueprints[:3]:
        current_start_time = time.time()
        geodes.append(optimize_blueprint(bp))
        print(f'Finished Blueprint {bp.id}, took {time.time() - current_start_time:.0f} seconds')
    print(f'Finished, took {time.time() - start_time:.0f} seconds total')
    prod = 1
    for g in geodes:
      prod *= g
    return prod

def main():
    # test = total_quality_levels('test_input.txt')
    # print(test, 'PASSED' if test == 33 else 'FAILED')
    # print()

    test = prod_geodes('input.txt')
    # print(test, 'PASSED' if test == 30 else 'FAILED')
    print(test)


if __name__ == '__main__':
    main()

# Basic Cache
# Test:  113, 745
# Input: 42, 71, 71

# Leaf pruning
# Test: 76, 549
# Input: 21, 37, 44

# Penultimate Leaf pruning
# Test: 65, 514
# Input: 12, 24, 38

# naive shortfall pruning
# Test: 66, 510
# Input: 4, 25, 38

# stop at max resource need (was buggy, with obs)
# Test: 44, 47
# Input: 1, 4, 19

# Naive headroom cap
# Test: 20, 19
# Input: 1, 5, 12

# fixed max res
# Test: 18, 17
# Input: 1, 4, 11

# More aggressive pruning
# Test: 7, 7
# Input: 0, 2, 4

# Impl
# 24  25  26  27  28  29  30  31  32
#  0   1   2   5   8  13  20  33  51
#  2   3   6  10  17  28  41  59  84
#  4   8  13  21  34  51  73 103 131

# 21840
