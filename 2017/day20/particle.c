#include "particle.h"
#include <inttypes.h>
#include <stdio.h>

int64_t
abs64(int64_t x)
{
    return (x < 0) ? -x : x;
}

int64_t
l1(struct V3 const p1, struct V3 const p2)
{
    return abs64(p1.x - p2.x) + abs64(p1.y - p2.y) + abs64(p1.z - p2.z);
}

struct V3 ORIGIN = { 0, 0, 0 };

struct Particle
parse_particle(char const * const s, size_t const idx)
{
    struct Particle p;
    sscanf(
        s, "p=<%ld,%ld,%ld>, v=<%ld,%ld,%ld>, a=<%ld,%ld,%ld>", &p.pos.x,
        &p.pos.y, &p.pos.z, &p.vel.x, &p.vel.y, &p.vel.z, &p.acc.x, &p.acc.y,
        &p.acc.z

    );
    p.idx = idx;
    return p;
}

struct V3
V3_add(struct V3 const a, struct V3 const b)
{
    struct V3 out = a;
    out.x += b.x;
    out.y += b.y;
    out.z += b.z;
    return out;
}

bool
V3_eq(struct V3 const a, struct V3 const b)
{
    return a.x == b.x && a.y == b.y && a.z == b.z;
}

struct Particle
move(struct Particle const particle)
{
    struct Particle out = particle;
    out.vel = V3_add(out.vel, out.acc);
    out.pos = V3_add(out.pos, out.vel);
    return out;
}

size_t
format_v3(char * restrict dst, const struct V3 v)
{
    return sprintf(dst, "<%ld,%ld,%ld>", v.x, v.y, v.z);
}

size_t
format_particle(char * restrict dst, const struct Particle particle)
{
    size_t written = 0;
    written += sprintf(dst + written, "%zu ", particle.idx);
    written += sprintf(dst + written, "p=");
    written += format_v3(dst + written, particle.pos);
    written += sprintf(dst + written, ", v=");
    written += format_v3(dst + written, particle.vel);
    written += sprintf(dst + written, ", a=");
    written += format_v3(dst + written, particle.acc);
    return written;
}

int
l1_difference(void const * const a, void const * const b)
{
    struct Particle * x = (struct Particle *)a;
    struct Particle * y = (struct Particle *)b;
    return l1((*x).pos, ORIGIN) - l1((*y).pos, ORIGIN);
}

int
particle_sort(const void * const a, const void * const b)
{
    int l1d = l1_difference(a, b);
    if (l1d) {
        return l1d;
    }
    struct Particle * x = (struct Particle *)a;
    struct Particle * y = (struct Particle *)b;
    if (x->pos.x != y->pos.x) {
        return x->pos.x - y->pos.x;
    }
    if (x->pos.y != y->pos.y) {
        return x->pos.y - y->pos.y;
    }
    if (x->pos.z != y->pos.z) {
        return x->pos.z - y->pos.z;
    }
    return 0;
}
