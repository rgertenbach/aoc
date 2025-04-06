#ifndef PARTICLE_H_
#define PARTICLE_H_

#include <stdbool.h>
#include <inttypes.h>
#include <stddef.h>

struct V3 {
    int64_t x, y, z;
};

struct Particle {
    size_t idx;
    struct V3 pos, vel, acc;
};

extern struct V3 ORIGIN;

// L1 (Manhattan) distance between two points.
int64_t l1(struct V3 const p1, struct V3 const p2);

extern struct Particle parse_particle(char const * const s, size_t const idx);

struct Particle move(struct Particle const Particle);

struct V3 V3_add(struct V3 const a, struct V3 const b);
bool V3_eq(struct V3 const a, struct V3 const b);

size_t format_particle(char * restrict dst, struct Particle const particle);

size_t format_v3(char * restrict dst, struct V3 const v);

// Can be used to sort by which particle is further from the origin.
int l1_difference(void const * const a, void const * const b);
int particle_sort(void const * const a, void const * const b);

size_t
remove_collisions(struct Particle * particles, size_t n);

size_t remove_collisions2(struct Particle * particles, size_t n);
#endif  // PARTICLE_H_
