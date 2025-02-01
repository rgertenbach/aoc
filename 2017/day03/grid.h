#ifndef GRID_H
#define GRID_H
#include <stdint.h>
enum Direction { D_RIGHT = 1, D_UP = 2, D_LEFT = 3, D_DOWN = 4 };

struct Point {
    int row;
    int col;
};

extern inline struct Point
move(struct Point const p, enum Direction d)
{
    switch (d) {
    case D_RIGHT:
        return (struct Point){ p.row, p.col + 1 };
        break;
    case D_UP:
        return (struct Point){ p.row - 1, p.col };
        break;
    case D_LEFT:
        return (struct Point){ p.row, p.col - 1 };
        break;
    case D_DOWN:
        return (struct Point){ p.row + 1, p.col };
        break;
    }
}

extern inline enum Direction
turn(enum Direction const d)
{
    switch (d) {
    case D_RIGHT:
        return D_UP;
        break;
    case D_UP:
        return D_LEFT;
        break;
    case D_LEFT:
        return D_DOWN;
        break;
    case D_DOWN:
        return D_RIGHT;
        break;
    }
}
#endif // GRID_H
