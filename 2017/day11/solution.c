#include "/home/robin/src/clib/string/split.h"
#include "grid.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLEN 22000
#define MOVELEN 3

struct Distances {
    int32_t end, furthest;
};

struct Distances
solution(char const * const s)
{
    int32_t furthest = 0;
    char ** moves = malloc(MAXLEN * sizeof(char *));
    for (size_t i = 0; i < MAXLEN; ++i) {
        moves[i] = malloc(MOVELEN);
    }
    size_t n_moves = strnsplit((char **)moves, s, ",", MAXLEN, MOVELEN);
    struct Position pos = { 0 };
    for (size_t i = 0; i < n_moves; ++i) {
        pos = move(pos, parse_move(moves[i]));
        if (distance(pos) > furthest) {
            furthest = distance(pos);
        }
    }
    for (size_t i = 0; i < MAXLEN; ++i) {
        free(moves[i]);
    }
    free(moves);
    return (struct Distances){ distance(pos), furthest };
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

    fgets(s, MAXLEN, f);
    s[strlen(s) - 1] = '\0';  // Trim newline.
    fclose(f);

    struct Distances d = solution(s);
    printf("Part 1: %d\nPart 2: %d\n", d.end, d.furthest);
    return 0;
}
