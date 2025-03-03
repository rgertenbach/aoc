#include "hash.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLEN 100

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

    struct Knot knot = { .length = MAX_KNOT_LEN };
    for (size_t i = 0; i < MAX_KNOT_LEN; ++i) {
        knot.arr[i] = i;
    }

    if (strcmp(argv[1], "input.txt")) {
        knot.length = 5;
    }

    char s[MAXLEN];
    fgets(s, MAXLEN, f);
    s[strlen(s) - 1] = '\0';  // Trim newline.
    char * c = s;
    fclose(f);
    size_t ks[MAXLEN] = { 0 };
    size_t nks = 0;
    while (*c != '\0') {
        if (*c == ',') {
            c++;
            nks++;
        }
        ks[nks] *= 10;
        ks[nks] += *c - '0';
        c++;
    }
    nks++;
    for (size_t i = 0; i < nks; ++i) {
        half_twist(&knot, ks[i]);
    }
    printf(
        "%d * %d = %d\n", knot.arr[0], knot.arr[1], knot.arr[0] * knot.arr[1]
    );

    return 0;
}
