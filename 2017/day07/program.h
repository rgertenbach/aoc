#ifndef PROG_H
#define PROG_H

#include <stddef.h>
#include <uthash.h>

#define PROG_MAX_CHILDREN 100
#define PROG_MAX_NAME_LEN 20

struct Program {
    char name[PROG_MAX_NAME_LEN];
    int weight;
    char ** children;
    size_t n_children;
};

struct Program * parse_program(char * s);

void destroy_program(struct Program * p);

struct Dependency {
    char name[PROG_MAX_NAME_LEN];
    char dep[PROG_MAX_NAME_LEN];
    UT_hash_handle hh;
};

struct Dependency *
get_dependency(struct Dependency * deps, char const * const name);

void add_dependency(
    struct Dependency ** deps,
    char const * const child,
    char const * const parent
);

void destroy_dependencies(struct Dependency * deps);

#endif  // PROG_H
