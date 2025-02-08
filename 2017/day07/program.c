#include "program.h"
#include "/home/robin/src/clib/string/split.h"
#include <ctype.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <uthash.h>

struct Program *
parse_program(char * s)
{
    struct Program * program = malloc(sizeof(struct Program));
    program->balance = BALANCE_UNKNOWN;
    program->total_weight = PROG_TOTAL_WEIGHT_UNKNOWN;
    size_t n = 0;

    // Parse name.
    while (*s != ' ') {
        program->name[n++] = *(s++);
    }
    program->name[n] = '\0';

    // Parse weight.
    s += 2;
    program->weight = 0;
    while (isdigit(*s)) {
        program->weight *= 10;
        program->weight += *(s++) - '0';
    }
    s++;

    if (*s == '\0') {
        program->n_children = 0;
        return program;
    }
    // Parse children
    s += 4;
    program->children = malloc(PROG_MAX_CHILDREN * sizeof(char *));
    for (size_t i = 0; i < PROG_MAX_CHILDREN; ++i) {
        program->children[i] = malloc(PROG_MAX_NAME_LEN);
    }
    program->n_children = strnsplit(
        program->children, s, ", ", PROG_MAX_CHILDREN, PROG_MAX_NAME_LEN
    );

    return program;
}

void
destroy_program(struct Program * p)
{
    for (size_t i = 0; i < PROG_MAX_CHILDREN; ++i) {
        free(p->children[i]);
    }
    free(p->children);
    free(p);
}

struct Program *
find_program(char const * const name, struct Program * programs)
{
    struct Program * program = NULL;
    HASH_FIND_STR(programs, name, program);
    if (!program) {
        fprintf(stderr, "Could not find program %s\n", name);
        exit(1);
    }
    return program;
}

struct Dependency *
get_dependency(struct Dependency * deps, char const * const name)
{
    struct Dependency * f = NULL;
    HASH_FIND_STR(deps, name, f);
    return f;
}

void
destroy_dependencies(struct Dependency * dep)
{
    free(dep);
}

void
add_dependency(
    struct Dependency ** deps,
    const char * const child,
    const char * const parent
)
{
    struct Dependency * d = malloc(sizeof(struct Dependency));
    strcpy(d->name, child);
    strcpy(d->dep, parent);
    HASH_ADD_STR(*deps, name, d);
}

int
calculate_total_weight(
    char const * const name, struct Program * const programs
)
{
    struct Program * p = find_program(name, programs);
    if (p->total_weight == PROG_TOTAL_WEIGHT_UNKNOWN) {
        p->balance = BALANCE_BALANCED;
        p->total_weight = p->weight;
        for (size_t i = 0; i < p->n_children; ++i) {
            p->total_weight
                += calculate_total_weight(p->children[i], programs);
            if (i > 0
                && calculate_total_weight(p->children[i], programs)
                       != calculate_total_weight(p->children[0], programs)) {
                p->balance = BALANCE_UNBALANCED;
            }
        }
    }
    return p->total_weight;
}

// Currently finds root, we need to find the lowest imbalanced node!
struct Program *
find_imbalanced(char const * const root, struct Program * programs)
{
    struct Program * p = find_program(root, programs);
    if (p->balance == BALANCE_BALANCED) {
        return NULL;
    }
    struct Program * child;
    for (size_t i = 0; i < p->n_children; ++i) {
        child = find_program(p->children[i], programs);
        if (child->balance == BALANCE_UNBALANCED) {
            return find_imbalanced(p->children[i], programs);
        }
    }
    return p;
}

struct WeightIndex {
    int weight;
    size_t index;
};

int WeightIndex_asc(void const * a, void const * b)
{
    struct WeightIndex const * x = a;
    struct WeightIndex const * y = b;
    return x->weight - y->weight;
}

int find_new_weight(struct Program const * const p, struct Program * programs)
{
    struct WeightIndex weights[PROG_MAX_CHILDREN];
    struct Program * child = NULL;
    for (size_t i = 0; i < p->n_children; ++i) {
        child = find_program(p->children[i], programs);
        weights[i] = (struct WeightIndex) {child->total_weight, i};
    }
    qsort(weights, p->n_children, sizeof(*weights), WeightIndex_asc);

    // We know it's at least 3.
    size_t tochange;
    int target_weight;
    if (weights[0].weight == weights[1].weight) {
        target_weight = weights[0].weight;
        tochange = weights[p->n_children - 1].index;
    } else {
        target_weight = weights[p->n_children - 1].weight;
        tochange = weights[0].index;
    }
    child = find_program(p->children[tochange], programs);
    return target_weight - (child->total_weight - child->weight);
}
