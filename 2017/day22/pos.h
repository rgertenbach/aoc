#ifndef POS_H
#define POS_H

#include <stdbool.h>
#include <stdint.h>
#include <uthash.h>

struct Position {
    int64_t row;
    int64_t col;
};

enum State {
    STATE_CLEAN = 0,
    STATE_WEAK = 1,
    STATE_INFECTED = 2,
    STATE_FLAGGED = 3,
};

struct PositionSet {
    UT_hash_handle hh;
    struct Position pos;
    enum State state;
};

enum Direction {
    DIR_NORTH = 1,
    DIR_EAST = 2,
    DIR_SOUTH = 3,
    DIR_WEST = 4,
};

struct Carrier {
    struct Position pos;
    enum Direction dir;
};

struct BurstResult {
    struct Carrier carrier;
    bool newly_infected;
};

struct PositionSet *
PositionSet_get(struct PositionSet ** set, struct Position pos);
void PositionSet_set(
    struct PositionSet ** set, struct Position pos, enum State state
);
void PositionSet_del(struct PositionSet ** set, struct Position pos);

enum Direction turn_left(enum Direction);
enum Direction turn_right(enum Direction);
enum Direction turn_around(enum Direction);
struct Carrier Carrier_move(struct Carrier carrier);

struct BurstResult
burst1(struct Carrier carrier, struct PositionSet ** infected);
struct BurstResult
burst2(struct Carrier carrier, struct PositionSet ** infected);
#endif  // POS_H
