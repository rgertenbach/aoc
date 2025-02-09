#include "op.h"
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLEN 1000

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
    char * s = malloc(MAXLEN);
    struct Op ops[20000];
    size_t nops = 0;

    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        ops[nops++] = parse(s);
    }
    fclose(f);

    struct Register * registers = NULL;
    int p1 = INT_MIN;
    int p2 = INT_MIN;
    int t;

    for (size_t i = 0; i < nops; ++i) {
        t = process(&registers, ops[i]);
        if (t > p2) {p2 = t;}
    }

    struct Register * t1, * t2;
    HASH_ITER(hh, registers, t1, t2) {
        if (t1->value > p1) {p1 = t1->value;}
    }
    printf("Part 1: %d\n", p1);
    printf("Part 2: %d\n", p2);
    return 0;
}
