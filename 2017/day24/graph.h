#ifndef GRAPH_H
#define GRAPH_H
#include <uthash.h>

struct Connection {
    uint64_t in;
    uint64_t out;
    uint64_t id;
};

struct Comp {
    uint64_t in;
    struct Connection out[64];
    size_t nout;
    UT_hash_handle hh;
};

struct Result {
    uint64_t strength;
    uint64_t length;
};

struct Comp * get(struct Comp ** components, uint64_t const in);

void destroy(struct Comp **); 

struct Result
best_path(uint64_t current, struct Comp * components, uint64_t visited);
struct Result
longest_path(uint64_t current, struct Comp * components, uint64_t visited);

#endif  // GRAPH_H
