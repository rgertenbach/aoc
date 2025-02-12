#ifndef HASH_H
#define HASH_H

#include <inttypes.h>
#include <stdlib.h>

#define MAX_KNOT_LEN 256

struct Knot {
    size_t length;
    size_t pos;
    size_t skip;
    uint8_t arr[MAX_KNOT_LEN];
};

void
half_twist(struct Knot * const knot, size_t const k)
{
    size_t left = knot->pos;
    size_t right = (left + k - 1) % knot->length;
    size_t off = k;
    while (off > 1) {
        uint8_t temp = knot->arr[left];
        knot->arr[left] = knot->arr[right];
        knot->arr[right] = temp;
        right = (right + knot->length - 1) % knot->length;
        left = (left + 1) % knot->length;
        off -= 2;
    }
    knot->pos += k + knot->skip++;
    knot->pos %= knot->length;
}

#endif  // HASH_H
