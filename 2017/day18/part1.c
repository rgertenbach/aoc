#include "part1.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LAST_SOUND

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
    char s[MAXLEN];

    struct Instruction instructions[100];
    size_t ninst = 0;
    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        instructions[ninst++] = parse(s);
    }
    fclose(f);

    int64_t registers[DUET_REGISTER_SZ] = { 0 };
    size_t p = 0;
    struct Result r;
    do {
        r = op(registers, instructions[p]);
        p += r.move;
    } while (!r.rec && p < ninst);
    printf("Part 1: %ld\n", registers[DUET_RECOVERED]);
    return 0;
}
