#include "pos.h"
#include <stdbool.h>
#include <uthash.h>

struct PositionSet *
PositionSet_has(struct PositionSet ** set, struct Position pos)
{
    struct PositionSet * f = NULL;
    HASH_FIND(hh, *set, &pos, sizeof(pos), f);
    return f;
}

void
PositionSet_add(struct PositionSet ** set, struct Position pos)
{
    if (PositionSet_has(set, pos)) { return; }
    struct PositionSet * new = malloc(sizeof(struct PositionSet));
    memcpy(&(new->pos), &pos, sizeof(pos));
    HASH_ADD(hh, *set, pos, sizeof(pos), new);
}

void
PositionSet_del(struct PositionSet ** set, struct Position pos)
{
    struct PositionSet * f = PositionSet_has(set, pos);
    if (f) {
        HASH_DEL(*set, f);
        free(f);
    }
}

enum Direction
turn_left(enum Direction dir)
{
    switch (dir) {
    case DIR_NORTH: return DIR_WEST;
    case DIR_WEST: return DIR_SOUTH;
    case DIR_SOUTH: return DIR_EAST;
    case DIR_EAST: return DIR_NORTH;
    }
}

enum Direction
turn_right(enum Direction dir)
{
    switch (dir) {
    case DIR_NORTH: return DIR_EAST; ;
    case DIR_WEST: return DIR_NORTH;
    case DIR_SOUTH: return DIR_WEST;
    case DIR_EAST: return DIR_SOUTH;
    }
}

struct Carrier
Carrier_move(struct Carrier carrier)
{
    switch (carrier.dir) {
    case DIR_NORTH: carrier.pos.row--; break;
    case DIR_EAST: carrier.pos.col++; break;
    case DIR_SOUTH: carrier.pos.row++; break;
    case DIR_WEST: carrier.pos.col--; break;
    }
	return carrier;
}

struct BurstResult
burst(struct Carrier carrier, struct PositionSet ** infected)
{
	bool newly_infected = false;
    if (PositionSet_has(infected, carrier.pos)) {
        carrier.dir = turn_right(carrier.dir);
        PositionSet_del(infected, carrier.pos);
    } else {
        carrier.dir = turn_left(carrier.dir);
        PositionSet_add(infected, carrier.pos);
		newly_infected = true;
    }
	carrier = Carrier_move(carrier);

	return (struct BurstResult) { carrier, newly_infected };
}
