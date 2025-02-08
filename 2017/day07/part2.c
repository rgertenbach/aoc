#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "program.h"
#include "program.h"

#define MAXLEN 1000


int main(int const argc, char const * const * const argv)
{
    if (argc < 2) {
        fprintf(stderr, "Need to supply filename\n");
        exit(1);
    }
    FILE * f = fopen(argv[1], "r");
    if (!f) {
        fprintf(stderr, "Could not open %s\n", argv[1]);
        exit(1);
    }
    char * s = malloc(MAXLEN);
    char program_names[2000][PROG_MAX_NAME_LEN];
    struct Program * programs = NULL;
    size_t n_programs = 0;
    struct Dependency * deps = NULL;
    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        struct Program * p = parse_program(s);
        HASH_ADD_STR(programs, name, p);
        strcpy(program_names[n_programs++], p->name);
        for (size_t i = 0; i < p->n_children; ++i) {
            add_dependency(&deps, p->children[i], p->name);
        }
    }
    fclose(f);

    struct Dependency * d = NULL;
    char root[PROG_MAX_NAME_LEN];
    for (size_t i = 0; i < n_programs; ++i) {
        d = get_dependency(deps, program_names[i]);
        if (!d) {
            strcpy(root, program_names[i]);
            break;
        }
    }
    printf("Part 1: %s\n", root);

    calculate_total_weight(root, programs);
    struct Program * imbalanced = find_imbalanced(root, programs);

    printf("Part 2: %d\n", find_new_weight(imbalanced, programs));
}
