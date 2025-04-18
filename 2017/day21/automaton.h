#ifndef AUTOMATON_H_
#define AUTOMATON_H_

#define GRID_MAX_N 1000
#include <stdlib.h>

typedef char Grid_t[GRID_MAX_N][GRID_MAX_N];

struct Pattern {
    char pattern[16];
    size_t stride;
};

struct Replacement {
    struct Pattern match;
    struct Pattern replacement;
};

struct Replacement parse_replacement(char const * const s);

struct Pattern pattern_at(
    size_t const row, size_t const col, Grid_t grid, size_t const stride
);

struct Pattern rotate_pattern(struct Pattern const p);
struct Pattern hflip_pattern(struct Pattern const p);
struct Pattern vflip_pattern(struct Pattern const p);

bool patterns_match(struct Pattern const p1, struct Pattern const p2);
struct Pattern find_replacement(
    struct Pattern p, struct Replacement * replacements, size_t n
);

size_t grow(
    Grid_t next_grid,
    Grid_t grid,
    size_t const grid_sz,
    struct Replacement * replacements,
    size_t const nrepl
);

size_t count(Grid_t grid, size_t n);

void format_pattern(char * const dest, struct Pattern const p);
void format_grid(char * dest, Grid_t grid, size_t const n);
#endif  // AUTOMATON_H_
