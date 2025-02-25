#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#ifndef GRID_H

#define abs(a) (((a) < 0) ? -(a) : (a))
#define min(a, b) (((a) < (b)) ? (a) : (b))
#define max(a, b) (((a) > (b)) ? (a) : (b))

enum Move { MOVE_NW = 1, MOVE_N, MOVE_NE, MOVE_SW, MOVE_S, MOVE_SE };

enum Move
parse_move(char const * const s)
{
    if (!strcmp(s, "nw")) {
        return MOVE_NW;
    }
    if (!strcmp(s, "n")) {
        return MOVE_N;
    }
    if (!strcmp(s, "ne")) {
        return MOVE_NE;
    }
    if (!strcmp(s, "sw")) {
        return MOVE_SW;
    }
    if (!strcmp(s, "s")) {
        return MOVE_S;
    }
    if (!strcmp(s, "se")) {
        return MOVE_SE;
    }
    exit(38);
}

struct Position {
    int32_t x, y, z;
};

struct Position
move(struct Position pos, enum Move move)
{
    struct Position out;
    memcpy(&out, &pos, sizeof(struct Position));
    switch (move) {
    case MOVE_NW:
        out.x++;
        out.y--;
        break;
    case MOVE_N:
        out.y--;
        out.z++;
        break;
    case MOVE_NE:
        out.x--;
        out.z++;
        break;
    case MOVE_SW:
        out.x++;
        out.z--;
        break;
    case MOVE_S:
        out.y++;
        out.z--;
        break;
    case MOVE_SE:
        out.x--;
        out.y++;
        break;
    }
    assert(pos.x + pos.y + pos.z == 0);
    return out;
}

int32_t
distance(struct Position pos)
{
    return max(abs(pos.x), max(abs(pos.y), abs(pos.z)));
}

#undef min
#undef abs
#define GRID_H
#endif  // GRID_H
