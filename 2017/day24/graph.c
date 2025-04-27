#include "graph.h"
#include <uthash.h>

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
    struct Comp * c, *n;
    HASH_ITER(hh, *components, c, n) {
        free(c);
    }
    free(*components);
    *components = NULL;
}

struct Comp * copy(struct Comp * old)
{
    struct Comp * new = old;
    struct Comp * c, *n;
    HASH_ITER(hh, old, c, n) {
        free(c);
    }
    return new;
}
