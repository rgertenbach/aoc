#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <uthash.h>
#include "graph.h"

#define MAXLEN 1000

int64_t
best_path(uint64_t current, struct Comp * components)
{
    struct Comp * a = get(&components, current);
    int64_t best = 0;
    int64_t add = 0;
    for (size_t i = 0; i < a->nout; ++i) {
        if (a->out[i] == current) {
            add += current;
        } else {
            int64_t s = best_path(a->out[i], components);
            if (s > best) { best = s; }
        }
    }
    return best + add;
}

int
main(int const argc, char const * const * const argv)
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
    char s[MAXLEN];
    struct Comp * components = NULL;

    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        uint64_t in, out;
        sscanf(s, "%ld/%ld", &in, &out);
        struct Comp * available = get(&components, in);
        available->out[available->nout++] = out;
        printf(
            "Added %ld for %ld, which now has %zu\n", out, in, available->nout
        );
    }
    fclose(f);
    printf("Part 1: %ld\n", best_path(0, components));
    return 0;
}
