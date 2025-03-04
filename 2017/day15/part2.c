#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MAXLEN 1000
unsigned long const AMUL = 16807;
unsigned long const BMUL = 48271;
unsigned long const DIV = 2147483647;
unsigned long const MASK16 = (1 << 16) - 1;

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

    unsigned long a = 0, b = 0;
    fscanf(f, "Generator A starts with %lu\n", &a);
    fscanf(f, "Generator B starts with %lu\n", &b);
    fclose(f);
    size_t matches = 0;
    for (size_t i = 0; i < 5000000; ++i) {
        do {
            a = (a * AMUL) % DIV;
        } while (a & 0b11);
        do {
            b = (b * BMUL) % DIV;
        } while (b & 0b111);
        if ((a & MASK16) == (b & MASK16)) {
            matches++;
        }
    }
    printf("Part 1: %zu\n", matches);

    return 0;
}
