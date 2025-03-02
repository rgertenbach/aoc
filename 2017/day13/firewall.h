#ifndef FIREWALL_H
#define FIREWALL_H

#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <uthash.h>

enum Direction {
    DIRECTION_UP = 1,
    DIRECTION_DOWN = 2,
};

struct Firewall {
    size_t layer;
    size_t range;        /// # of elements
    size_t pos;          /// Position of security scanner.
    enum Direction dir;  // Direction the scanner is moving.
    UT_hash_handle hh;
};

size_t
pos_steps_from_now(struct Firewall const * const fw, size_t step)
{

    enum Direction dir = fw->dir;
    size_t pos = fw->pos;
    size_t phase = (fw->range - 1) * 2;
    step %= phase;

    while (step) {
        switch (dir) {
        case DIRECTION_DOWN:
            pos += step;
            if (pos >= fw->range) {
                dir = DIRECTION_UP;
                step = pos % fw->range;
                pos = fw->range - 1;
            }
            step = 0;
            break;
        case DIRECTION_UP:
            if (step < pos) {
                pos -= step;
                step = 0;
            } else {
                step -= pos;
                pos = 0;
                dir = DIRECTION_DOWN;
            }
            break;
        default:
            break;
        }
    }

    return pos;
}

struct Firewall *
fw_get(struct Firewall * fw, size_t const layer)
{
    struct Firewall * f = NULL;
    HASH_FIND_INT(fw, &layer, f);
    return f;
}

bool
fw_has(struct Firewall * fw, size_t const layer)
{
    return fw_get(fw, layer) != NULL;
}

void
fw_add(struct Firewall ** fw, size_t const layer, size_t const size)
{
    struct Firewall * l = malloc(sizeof(struct Firewall));
    l->layer = layer;
    l->range = size;
    l->dir = DIRECTION_DOWN;
    HASH_ADD_INT(*fw, layer, l);
}

size_t
severity(struct Firewall * l)
{
    return l->layer * l->range;
}

#endif  // FIREWALL_H
