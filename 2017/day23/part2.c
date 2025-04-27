#include "proc.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLEN 1000
#define REG_A registers['a' - 'a']
#define REG_B registers['b' - 'a']
#define REG_C registers['c' - 'a']
#define REG_D registers['d' - 'a']
#define REG_E registers['e' - 'a']
#define REG_F registers['f' - 'a']
#define REG_G registers['g' - 'a']
#define REG_H registers['h' - 'a']

bool
isprime(int64_t x, int64_t * primes, size_t nprimes)
{
    for (size_t i = 0; i < nprimes; ++i) {
        if (x % primes[i] == 0) { return false; }
        if (primes[i] * primes[i] > x) { return true; }
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
    char s[MAXLEN];
    struct Instruction instructions[32];
    size_t ninst = 0;

    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        instructions[ninst++] = parse(s);
    }
    fclose(f);

    int64_t * primes = malloc(123500 / 2 * sizeof(int64_t));
    size_t nprimes = 0;
    primes[nprimes++] = 2;
    for (int64_t c = 3; c < 123500 / 2; c += 2) {
        if (isprime(c, primes, nprimes)) { primes[nprimes++] = c; }
    }

    int64_t registers[PROC_REGISTER_SZ] = { 1 };
    size_t p = 0;
    struct Result r;
    while (p < ninst) {
        r = op(registers, instructions[p]);
        if (p == 7) { break; }
        p += r.move;
    }
    for (int64_t x = REG_B; x <= REG_C; x += 17) {
        REG_H += !isprime(x, primes, nprimes);
    }

    printf("Part 2: %ld\n", REG_H);
    return 0;
}
