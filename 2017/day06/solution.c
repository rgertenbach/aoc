#include "/home/robin/src/clib/string/split.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <uthash.h>

#define MAXLEN 1000
#define MAXBANKS 16

struct State {
    int banks[MAXBANKS];
    size_t n_banks;
    size_t cycles;
    UT_hash_handle hh;
};

struct State *
make_state(int const * const banks, size_t const n_banks, size_t const cycles)
{
    struct State * out = malloc(sizeof(struct State));
    memcpy(out->banks, banks, n_banks * sizeof(*banks));
    out->n_banks = n_banks;
    out->cycles = cycles;
    return out;
}

void
reallocate(int * banks, size_t const n_banks)
{
    size_t maxi = 0;
    for (size_t i = 1; i < n_banks; ++i) {
        if (banks[i] > banks[maxi]) {
            maxi = i;
        }
    }
    int amt = banks[maxi];
    int each = amt / n_banks;
    size_t rem = amt % n_banks;
    banks[maxi] = 0;
    for (size_t i = 0; i < n_banks; ++i) {
        banks[(maxi + i) % n_banks] += each;
    }
    for (size_t i = 0; i < rem; ++i) {
        banks[(maxi + i + 1) % n_banks]++;
    }
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
    char * s = malloc(MAXLEN);
    fgets(s, MAXLEN, f);
    fclose(f);
    s[strlen(s) - 1] = '\0';  // Trim newline.
    char ** str_banks = malloc(MAXBANKS * sizeof(char *));
    for (size_t i = 0; i < MAXBANKS; ++i) {
        str_banks[i] = malloc(MAXLEN);
    }
    size_t n_banks = strnsplit(str_banks, s, "\t", MAXBANKS, MAXLEN);
    int banks[MAXBANKS];
    for (size_t i = 0; i < n_banks; ++i) {
        banks[i] = atoi(str_banks[i]);
    }
    size_t cycles = 0;
    struct State * state_set = NULL;
    while (true) {
        struct State * state = make_state(banks, n_banks, cycles);
        struct State * f = NULL;
        HASH_FIND(hh, state_set, state->banks, n_banks * sizeof(*banks), f);
        if (f) {
            printf("%zu after %zu\n", cycles, cycles - f->cycles);
            break;
        }
        HASH_ADD(hh, state_set, banks, n_banks * sizeof(*banks), state);
        reallocate(banks, n_banks);
        cycles++;
    }
}
