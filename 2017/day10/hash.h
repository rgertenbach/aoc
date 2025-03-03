#ifndef HASH_H
#define HASH_H

#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_KNOT_LEN 256
#define HASH_ENTROPY 128
#define HASH_ELEMS 16
#define HASH_LEN 32

struct Knot {
    size_t length;
    uint8_t pos;
    uint8_t skip;
    uint8_t arr[MAX_KNOT_LEN];
};

void
half_twist(struct Knot * const knot, size_t const k)
{
    uint8_t left = knot->pos;
    uint8_t right = left + k - 1;
    size_t off = k;
    while (off > 1) {
        uint8_t temp = knot->arr[left];
        knot->arr[left] = knot->arr[right];
        knot->arr[right] = temp;
        right = right + knot->length - 1;
        left++;
        off -= 2;
    }
    knot->pos += k + knot->skip++;
}

/// @param h The destination to store the hash in.
/// @param ks The input to hash.
/// @param nks The length of the input.
void
hash(uint8_t * const h, char const * const ks, size_t const nks)
{
    // 0-Initialize hash output.
    memset(h, 0, HASH_ELEMS * sizeof(*h));
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
        half_twist(&knot, 17);
        half_twist(&knot, 31);
        half_twist(&knot, 73);
        half_twist(&knot, 47);
        half_twist(&knot, 23);
    }
    // Calculate dense hash.
    for (size_t i = 0; i < MAX_KNOT_LEN; ++i) {
        h[i / HASH_ELEMS] ^= knot.arr[i];
    }
}

void
tohex(char * dst, uint8_t const * h)
{
    for (size_t i = 0; i < HASH_ELEMS; ++i) {
        sprintf(dst + 2 * i, "%02x", h[i]);
    }
    dst[HASH_LEN] = '\0';
}

#endif  // HASH_H
