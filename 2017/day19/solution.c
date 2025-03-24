#include "state.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLEN 500

#define HORIZONTAL

size_t
find_start_col(char const * const row)
{
    for (size_t i = 0; row[i] != '\0'; ++i) {
        if (row[i] == '|') {
            return i;
        }
    }
    exit(1);
}

struct State
move(struct State state, char map[MAXLEN][MAXLEN])
{

    struct State out = advance(state);
    out.tile = map[out.row][out.col];
    if (out.tile == ' ') {
        out.dir = DIR_DONE;
        return out;
    }
    if (out.tile != '+') {
        return out;
    }

    if (out.dir == DIR_NORTH || out.dir == DIR_SOUTH) {
        if (is_accessible(map[out.row][out.col - 1], DIR_WEST)) {
            out.dir = DIR_WEST;
        } else {
            out.dir = DIR_EAST;
        }
    } else {
        if (is_accessible(map[out.row - 1][out.col], DIR_NORTH)) {
            out.dir = DIR_NORTH;
        } else {
            out.dir = DIR_SOUTH;
        }
    }

    return out;
}

int
main(int const argc, char const * const * const argv)
{
    if (argc < 2) {
        fprintf(stderr, "Need to supply filename\n");
        exit(1);
    }
    FILE * f = fopen(argv[1], "r");
    if (!f) {
        fprintf(stderr, "Could not open %s\n", argv[1]);
        exit(1);
    }
    char s[MAXLEN];
    char map[MAXLEN][MAXLEN];
    size_t rows = 0;
    size_t start_col;

    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        strcpy(map[rows++], s);
        if (rows == 1) {
            start_col = find_start_col(s);
        }
    }
    fclose(f);

    char part1[26];
    size_t sz = 0;
    size_t steps = 0;

    struct State state = { 0, start_col, DIR_SOUTH, '|' };

    while (state.dir != DIR_DONE) {
        state = move(state, map);
        steps++;
        if (isalpha(state.tile)) {
            part1[sz++] = state.tile;
        }
    }
    part1[sz] = '\0';
    printf("Part 1: %s\nPart 2: %zu\n", part1, steps);

    return 0;
}
