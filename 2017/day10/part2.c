#include "clist.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLEN 100

void
hash(uint8_t * const h, char const * const ks, size_t const nks)
{
    // 0-Initialize hash output.
    for (size_t i = 0; i < 16; ++i) {
        h[i] = 0;
    }
    // Initialize knot
    struct Knot knot = { .length = MAX_KNOT_LEN };
    for (size_t i = 0; i < MAX_KNOT_LEN; ++i) {
        knot.arr[i] = i;
    }
    // Calculate sparse hash.
    for (size_t i = 0; i < 64; ++i) {
        for (size_t k = 0; k < nks; ++k) {
            half_twist(&knot, ks[k]);
        }
    }
    // Calculate dense hash.
    for (size_t i = 0; i < MAX_KNOT_LEN; ++i) {
        h[i / 16] ^= knot.arr[i];
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


    char s[MAXLEN];
    fgets(s, MAXLEN, f);
    size_t len = strlen(s);
    if (s[len - 1] == '\n') {
        s[len - 1] = '\0';  // Trim newline.
    }
    fclose(f);

    char * c = s;
    char ks[MAXLEN] = { 0 };
    size_t nks = 0;
    while (*c != '\0') {
        ks[nks++] = (char)*c++;
    }
    ks[nks++] = 17;
    ks[nks++] = 31;
    ks[nks++] = 73;
    ks[nks++] = 47;
    ks[nks++] = 23;
    uint8_t h[16] = {0};
    hash(h, ks, nks);
    for (size_t i = 0; i < 16; ++i) {
        printf("%02x", h[i]);
    }
    printf("\n");

    return 0;
}
