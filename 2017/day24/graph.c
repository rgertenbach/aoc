#include "graph.h"
#include <uthash.h>

static uint64_t popcount(uint64_t x)
{
    uint64_t out = 0;
    while (x) {
        out += x & 1;
        x >>= 1;
    }
    return out;
}

struct Comp *
get(struct Comp ** components, uint64_t const in)
{
    struct Comp * f = NULL;
    HASH_FIND_INT(*components, &in, f);
    if (f == NULL) {
        f = malloc(sizeof(struct Comp));
        f->in = in;
        f->nout = 0;
        HASH_ADD_INT(*components, in, f);
    }
    return f;
}

void
destroy(struct Comp ** components)
{
    struct Comp *c, *n;
    HASH_ITER(hh, *components, c, n) { free(c); }
    free(*components);
    *components = NULL;
}

struct Result
best_path(uint64_t current, struct Comp * components, uint64_t visited)
{
    struct Comp * a = get(&components, current);
    uint64_t best = 0;
    for (size_t i = 0; i < a->nout; ++i) {
        if (visited & a->out[i].id) { continue; }
        struct Result s =
            best_path(a->out[i].out, components, visited | a->out[i].id);
        if (s.strength + current + a->out[i].out > best) {
            best = s.strength + current + a->out[i].out;
        }
    }
    return (struct Result){ best, visited };
}

struct Result
longest_path(uint64_t current, struct Comp * components, uint64_t visited)
{
    struct Comp * a = get(&components, current);
    struct Result best = { 0, popcount(visited) };
    for (size_t i = 0; i < a->nout; ++i) {
        if (visited & a->out[i].id) { continue; }
        struct Result s = longest_path(
            a->out[i].out, components, visited | a->out[i].id
        );
        s.strength += current + a->out[i].out;

        if (s.length > best.length
            || (s.length == best.length && s.strength > s.length)) {
            best = s;
        }
    }
    return best;
}
