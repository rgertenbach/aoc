#ifndef GRAPH_H
#define GRAPH_H
#include <uthash.h>

struct Comp {
    uint64_t in;
    uint64_t out[64];
    size_t nout;
    UT_hash_handle hh;
};

struct Comp * get(struct Comp ** components, uint64_t const in);

struct Comp * copy(struct Comp * components);
void destroy(struct Comp **); 


#endif  // GRAPH_H
