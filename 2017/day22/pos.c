#include "pos.h"
#include <stdbool.h>
#include <stdio.h>
#include <uthash.h>

struct PositionSet *
PositionSet_get(struct PositionSet ** set, struct Position pos)
{
    struct PositionSet * f = NULL;
    HASH_FIND(hh, *set, &pos, sizeof(pos), f);
    if (f == NULL) {
        f = malloc(sizeof(*f));
        f->pos = pos;
        f->state = STATE_CLEAN;
        HASH_ADD(hh, *set, pos, sizeof(pos), f);
    }

    return f;
}

void
PositionSet_set(
    struct PositionSet ** set, struct Position pos, enum State state
)
{
    struct PositionSet * setting = PositionSet_get(set, pos);
    setting->state = state;
}

void
PositionSet_del(struct PositionSet ** set, struct Position pos)
{
    struct PositionSet * f = PositionSet_get(set, pos);
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

enum Direction
turn_around(enum Direction dir)
{
    switch (dir) {
    case DIR_NORTH: return DIR_SOUTH;
    case DIR_WEST: return DIR_EAST;
    case DIR_SOUTH: return DIR_NORTH;
    case DIR_EAST: return DIR_WEST;
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
burst1(struct Carrier carrier, struct PositionSet ** infected)
{
    struct PositionSet * pos = PositionSet_get(infected, carrier.pos);
    switch (pos->state) {
    case STATE_INFECTED:
        pos->state = STATE_CLEAN;
        carrier.dir = turn_right(carrier.dir);
        break;
    case STATE_CLEAN:
        pos->state = STATE_INFECTED;
        carrier.dir = turn_left(carrier.dir);
        break;
    default: break;
    }

    carrier = Carrier_move(carrier);

    return (struct BurstResult){ carrier, pos->state == STATE_INFECTED };
}

struct BurstResult
burst2(struct Carrier carrier, struct PositionSet ** infected)
{
    struct PositionSet * pos = PositionSet_get(infected, carrier.pos);
    switch (pos->state) {
    case STATE_INFECTED:
        pos->state = STATE_FLAGGED;
        carrier.dir = turn_right(carrier.dir);
        break;
    case STATE_FLAGGED:
        pos->state = STATE_CLEAN;
        carrier.dir = turn_around(carrier.dir);
        break;
    case STATE_CLEAN:
        pos->state = STATE_WEAK;
        carrier.dir = turn_left(carrier.dir);
        break;
    case STATE_WEAK:
        pos->state = STATE_INFECTED;
        break;

    }

    carrier = Carrier_move(carrier);

    return (struct BurstResult){ carrier, pos->state == STATE_INFECTED };
}
