#include "dance.h"
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

#define REPS 1000000000

bool is_sorted(uint8_t programs[])
{
    for (size_t i = 1; i < N_PROG; ++i) {
        if (programs[i] <= programs[i-1]) { return false; }
    }
    return true;
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
    uint8_t programs[N_PROG];
    for (size_t i = 0; i < N_PROG; ++i) {
        programs[i] = i + 'a';
    }
    struct Instruction instruction;
    struct Instruction instructions[100000];
    size_t ninst = 0;
    while (1) {
        instruction = parse(f);
        if (instruction.kind == KIND_DONE) {
            break;
        }
        instructions[ninst++] = instruction;
    }

    size_t iter = 1;
    process_instructions(programs, instructions, ninst);
    printf("Part 1: ");
    print_progs(programs);

    while (!is_sorted(programs)) {
        iter++;
        process_instructions(programs, instructions, ninst);
    }
    size_t remaining = REPS % iter;
    for (size_t i = 0; i < remaining; ++i) {
        process_instructions(programs, instructions, ninst);
    }
    printf("Part 2: ");
    print_progs(programs);

    return 0;
}
