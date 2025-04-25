#ifndef POS_H
#define POS_H

#include <stdbool.h>
#include <stdint.h>
#include <uthash.h>

struct Position {
    int64_t row;
    int64_t col;
};

struct PositionSet {
    UT_hash_handle hh;
    struct Position pos;
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
PositionSet_has(struct PositionSet ** set, struct Position pos);
void PositionSet_add(struct PositionSet ** set, struct Position pos);
void PositionSet_del(struct PositionSet ** set, struct Position pos);

enum Direction turn_left(enum Direction);
enum Direction turn_right(enum Direction);
struct Carrier Carrier_move(struct Carrier carrier);

struct BurstResult
burst(struct Carrier carrier, struct PositionSet ** infected);
#endif  // POS_H
