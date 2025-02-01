#include "grid.h"
#include "uthash.h"
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#define INPUT 289326
#define abs(a) ((a) < 0 ? -(a) : a)

struct Square {
    struct Point point;
    int64_t value;
    UT_hash_handle hh;
};

void
add(struct Square ** grid, int const row, int const col, int64_t const value)
{
    struct Square * square = malloc(sizeof(struct Square));
    square->point.row = row;
    square->point.col = col;
    square->value = value;
    HASH_ADD(hh, *grid, point, sizeof(struct Point), square);
}

int64_t
get(struct Square * grid, int const row, int const col)
{
    struct Square lookup = { .point = { .row = row, .col = col } };
    struct Square * result;

    HASH_FIND(hh, grid, &lookup.point, sizeof(struct Point), result);
    if (result == NULL) {
        return 0;
    }
    return result->value;
}

int
main(void)
{
    int min_row = 0;
    int max_row = 0;
    int min_col = 0;
    int max_col = 0;
    bool part2_done = false;
    struct Point p = { .row = 0, .col = 0 };
    int current = 1;
    struct Square * grid = NULL;
    add(&grid, p.row, p.col, current);
    enum Direction d = D_RIGHT;
    while (current < INPUT) {
        if (p.col > max_col) {
            max_col = p.col;
            d = turn(d);
        } else if (p.row < min_row) {
            min_row = p.row;
            d = turn(d);
        } else if (p.col < min_col) {
            min_col = p.col;
            d = turn(d);
        } else if (p.row > max_row) {
            max_row = p.row;
            d = turn(d);
        }
        p = move(p, d);
        ++current;
        add(&grid, p.row, p.col,
            get(grid, p.row - 1, p.col - 1) + get(grid, p.row - 1, p.col)
                + get(grid, p.row - 1, p.col + 1) + get(grid, p.row, p.col - 1)
                + get(grid, p.row, p.col + 1) + get(grid, p.row + 1, p.col - 1)
                + get(grid, p.row + 1, p.col)
                + get(grid, p.row + 1, p.col + 1));
        if (!part2_done && get(grid, p.row, p.col) > INPUT) {
            printf("Part 2: %ld\n", get(grid, p.row, p.col));
            part2_done = true;
        };
    }
    printf("Part 1: %d\n", abs(p.row) + abs(p.col));
}
