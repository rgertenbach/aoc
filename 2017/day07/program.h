#ifndef PROG_H
#define PROG_H

#include <stddef.h>
#include <uthash.h>

#define PROG_MAX_CHILDREN 100
#define PROG_MAX_NAME_LEN 20
#define PROG_TOTAL_WEIGHT_UNKNOWN -1

enum Balance {
    BALANCE_UNKNOWN = 0,
    BALANCE_BALANCED = 1,
    BALANCE_UNBALANCED = 2
};

struct Program {
    char name[PROG_MAX_NAME_LEN];
    int weight;
    int total_weight;
    enum Balance balance;
    char ** children;
    size_t n_children;
    UT_hash_handle hh;
};

struct Program * parse_program(char * s);

struct Program *
find_program(char const * const name, struct Program * programs);

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

int calculate_total_weight(
    char const * const name, struct Program * const programs
);

struct Program *
find_imbalanced(char const * const root, struct Program * programs);

int find_new_weight(struct Program const * const p, struct Program * programs);

#endif  // PROG_H
