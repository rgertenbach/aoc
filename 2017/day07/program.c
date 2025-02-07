#include "program.h"
#include "/home/robin/src/clib/string/split.h"
#include <ctype.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <uthash.h>

struct Program *
parse_program(char * s)
{
    struct Program * program = malloc(sizeof(struct Program));
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

    // Parse children
    s += 5;
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
