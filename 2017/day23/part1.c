#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "proc.h"

#define MAXLEN 1000

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
    struct Instruction instructions[32];
    size_t ninst = 0;

    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        instructions[ninst++] = parse(s);
    }
    fclose(f);


    int64_t registers[PROC_REGISTER_SZ] = {0};
    size_t p = 0;
    struct Result r;
    size_t part1 = 0;
    while (p < ninst) {
        r = op(registers, instructions[p]);
        part1 += r.mul;
        p += r.move;

    }
    printf("Part 1: %zu\n", part1);
    return 0;
}
