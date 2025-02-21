#ifndef HASH_H
#define HASH_H

#include <inttypes.h>
#include <stdlib.h>

#define MAX_KNOT_LEN 256

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

#endif  // HASH_H
