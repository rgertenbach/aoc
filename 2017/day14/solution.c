#include "../day10/hash.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLEN 1000

bool
hexbit(char const * const hex, size_t i)
{
    size_t which = i / 4;
    i %= 4;
    i = 3 - i;  // reverse endianness.
    char const c = hex[which];
    uint8_t x = c - (isalpha(c) ? 'a' - 10 : '0');
    return x & (1 << i);
}

void
fbits(char * s, char const * const hex)
{
    for (size_t i = 0; i < HASH_ENTROPY; ++i) {
        s[i] = hexbit(hex, i) ? '#' : '.';
    }
    s[HASH_ENTROPY] = '\0';
}

size_t count_blocked(char const * s)
{
    size_t n = 0;
    while (*s) { n += (*s++ == '#');}
    return n;
}

int
main(int const argc, char const * const * const argv)
{
    if (argc < 2) {
        fprintf(stderr, "Need to supply input\n");
        exit(1);
    }
    char key[MAXLEN];
    uint8_t h[HASH_LEN] = { 0 };
    char hex[HASH_LEN + 1];
    char maprow[HASH_ENTROPY + 1];

    size_t n = 0;
    for (size_t row = 0; row < 128; ++row) {
        size_t keylen = sprintf(key, "%s-%zu", argv[1], row);
        hash(h, key, keylen);
        tohex(hex, h);
        fbits(maprow, hex);
        n += count_blocked(maprow);
    }
    printf("Part 1: %zu\n", n);
    return 0;
}
