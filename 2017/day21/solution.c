#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "automaton.h"

#define MAXLEN 10000

int main(int const argc, char const * const * const argv)
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

    struct Replacement replacements[MAXLEN];
    size_t n_replacements = 0;

    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        replacements[n_replacements++] = parse_replacement(s);
    }
    fclose(f);

    Grid_t grid; 
    grid_init(grid);
    Grid_t next_grid;
    grid_init(next_grid);
    strcpy(grid[0], ".#.");
    strcpy(grid[1], "..#");
    strcpy(grid[2], "###");
    size_t n = 3;

    for (size_t i = 0; i < 18; ++i) {
        n = grow(next_grid, grid, n, replacements, n_replacements);
        grid_copy(grid, next_grid);
        printf("Step %zu: %zu n: %zu\n", i + 1, count(grid, n), n);

    }

    return 0;
}
