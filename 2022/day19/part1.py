from typing import Iterable, Optional
from collections import namedtuple, Counter
import re
import time 

CYCLES = 24
ORE = 'ore'
CLAY = 'clay'
OBS = 'obsidian'
GEODE = 'geode'

Resources = namedtuple('Resources', [ORE, CLAY, OBS, GEODE])
Blueprint = namedtuple('Blueprint', ['id', ORE, CLAY, OBS, GEODE])


def parse_costs(costs: str) -> Resources:
    costs = re.sub('Each \w+ robot costs ', '', costs)
    costs = costs.rstrip('.')
    costs = costs.split(' and ')
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

def cumsum(n: int) -> int:
    return (n * (n + 1)) // 2

def naive_geode_headroom(robot_geodes, current, remaining):
    return current + remaining * robot_geodes + cumsum(remaining)



def optimize_one_step(
        robots: Resources, 
        resources: Resources, 
        cycle: int, 
        blueprint: Blueprint,
        cache: dict[tuple[Resources, Resources, int], int]) -> int:
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
    if not robots.geode and has_naive_resource_shortfall(resources, robots, blueprint, CYCLES - cycle - 1):
        return 0

    if naive_geode_headroom(robots.geode, resources.geode, CYCLES - cycle) < cache['most_geodes']:
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
    if robots.obsidian < max_clay_need:
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
    cache = {'most_geodes': 0}
    return optimize_one_step(robots, resources, 0, blueprint, cache)


def total_quality_levels(filename: str):
    print(filename)
    blueprints = load_data(filename)
    quality_levels = []
    start_time = time.time()
    for bp in blueprints:#[:3]:
        current_start_time = time.time()
        geodes = optimize_blueprint(bp)
        quality_level = bp.id * geodes
        quality_levels.append(quality_level)
        print(f'Finished Blueprint {bp.id}, took {time.time() - current_start_time:.0f} seconds')
    print(f'Finished, took {time.time() - start_time:.0f} seconds total')
    return sum(quality_levels)


def main():
    test = total_quality_levels('test_input.txt')
    print(test, 'PASSED' if test == 33 else 'FAILED')
    print()

    test = total_quality_levels('input.txt')
    print(test, 'PASSED' if test == 30 else 'FAILED')


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

# stop at max resource need
# Test: 44, 47
# Input: 1, 4, 19

# Naive headroom cap
# Test: 20, 19
# Input: 1, 5, 12
