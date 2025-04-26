#include "pos.h"
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLEN 1000

char const INFECTED = '#';


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
    struct PositionSet * infected1 = NULL;
    struct PositionSet * infected2 = NULL;

    int64_t rows = 0;
    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        for (int64_t col = 0; s[col] != '\0'; ++col) {
            if (s[col] == INFECTED) {
                PositionSet_set(&infected1, (struct Position) {rows, col}, STATE_INFECTED);
                PositionSet_set(&infected2, (struct Position) {rows, col}, STATE_INFECTED);
            }
        }
        rows++;
    }
    fclose(f);

    struct Carrier carrier = {.pos = {rows / 2, rows / 2}, DIR_NORTH};
    struct BurstResult result;
    size_t newly_infected = 0;
    for (size_t i = 0; i < 10000; ++i) {
        result = burst1(carrier, &infected1);
        newly_infected += result.newly_infected;
        carrier = result.carrier;
    }
    printf("Part 1: %zu\n", newly_infected);
    carrier = (struct Carrier) {.pos = {rows / 2, rows / 2}, DIR_NORTH};
    newly_infected = 0;
    for (size_t i = 0; i < 10000000; ++i) {
        result = burst2(carrier, &infected2);
        newly_infected += result.newly_infected;
        carrier = result.carrier;
    }
    printf("Part 2: %zu\n", newly_infected);
    return 0;
}
