#include "../day10/hash.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <uthash.h>

#define MAXLEN 1000
#define N HASH_ENTROPY

struct Point {
    uint8_t row;
    uint8_t col;
    UT_hash_handle hh;
};

bool
has_point(struct Point * set, uint8_t const row, uint8_t const col)
{
    struct Point p = { .row = row, .col = col };
    struct Point * f = NULL;
    HASH_FIND(
        hh, set, &p.row, offsetof(struct Point, col) + sizeof(uint8_t), f
    );
    return f != NULL;
}

void
add_point(struct Point ** set, uint8_t const row, uint8_t const col)
{
    struct Point * p = malloc(sizeof(struct Point));
    p->row = row;
    p->col = col;
    HASH_ADD(hh, *set, row, offsetof(struct Point, col) + sizeof(col), p);
}

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

size_t
count_blocked(char const * s)
{
    size_t n = 0;
    while (*s) {
        n += (*s++ == '#');
    }
    return n;
}

void
dfs(char * grid, size_t row, size_t col, struct Point ** visited)
{
    struct Point stack[10000];
    struct Point p;
    size_t n = 0;
    stack[n++] = (struct Point){ .row = row, .col = col };
    while (n) {
        p = stack[--n];
        size_t r = p.row, c = p.col;
        if (r > 0 && grid[(r - 1) * N + c] == '#'
            && !has_point(*visited, r - 1, c)) {
            add_point(visited, r - 1, c);
            stack[n++] = (struct Point){ .row = r - 1, .col = c };
        }
        if (r < N - 1 && grid[(r + 1) * N + c] == '#'
            && !has_point(*visited, r + 1, c)) {
            add_point(visited, r + 1, c);
            stack[n++] = (struct Point){ .row = r + 1, .col = c };
        }
        if (c > 0 && grid[r * N + c - 1] == '#'
            && !has_point(*visited, r, c - 1)) {
            add_point(visited, r, c - 1);
            stack[n++] = (struct Point){ .row = r, .col = c - 1 };
        }
        if (c < N - 1 && grid[r * N + c + 1] == '#'
            && !has_point(*visited, r, c + 1)) {
            add_point(visited, r, c + 1);
            stack[n++] = (struct Point){ .row = r, .col = c + 1 };
        }
    }
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
    char maprow[N + 1];
    char grid[N * N + 1];

    size_t n = 0;
    for (size_t row = 0; row < N; ++row) {
        size_t keylen = sprintf(key, "%s-%zu", argv[1], row);
        hash(h, key, keylen);
        tohex(hex, h);
        fbits(maprow, hex);
        n += count_blocked(maprow);
        strcpy(grid + row * N, maprow);
    }
    printf("Part 1: %zu\n", n);

    size_t regions = 0;
    struct Point * visited = NULL;

    for (size_t row = 0; row < 128; ++row) {
        for (size_t col = 0; col < 128; ++col) {
            if (grid[row * N + col] == '#' && !has_point(visited, row, col)) {
                regions++;
                dfs(grid, row, col, &visited);
            }
        }
    }
    printf("Part 2: %zu\n", regions);
    return 0;
}
