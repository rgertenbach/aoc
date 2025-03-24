#ifndef STATE_H_
#define STATE_H_
#include <stdbool.h>
#include <stdlib.h>

enum Direction {
    DIR_NORTH = 1,
    DIR_EAST = 2,
    DIR_SOUTH = 3,
    DIR_WEST = 4,
    DIR_DONE = 5,
};

char *
fdir(enum Direction d)
{
    switch (d) {
    case DIR_NORTH:
        return "North";
    case DIR_EAST:
        return "East";
    case DIR_SOUTH:
        return "South";
    case DIR_WEST:
        return "West";
    case DIR_DONE:
        return "Done";
    }
}

struct State {
    size_t row;
    size_t col;
    enum Direction dir;
    char tile;
};

// Whether the tile can be moved to given the current direction.
bool
is_accessible(char const c, enum Direction d)
{
    switch (d) {
    case DIR_NORTH:
    case DIR_SOUTH:
        return c != ' ' && c != '-';
        break;
    case DIR_WEST:
    case DIR_EAST:
        return c != ' ' && c != '|';
        break;
    default:
        return false;
        break;
    }
}

struct State
advance(struct State in)
{
    struct State out = in;
    switch (in.dir) {
    case DIR_NORTH:
        out.row--;
        break;
    case DIR_SOUTH:
        out.row++;
        break;
    case DIR_WEST:
        out.col--;
        break;
    case DIR_EAST:
        out.col++;
        break;
    default:
        break;
    }
    return out;
}

#endif  // STATE_H_
