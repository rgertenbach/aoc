#include "graph.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <uthash.h>

#define MAXLEN 1000

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
    uint64_t id = 1;
    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        uint64_t in, out;
        sscanf(s, "%ld/%ld", &in, &out);
        struct Comp * available = get(&components, in);
        available->out[available->nout++] = (struct Connection){ in, out, id };
		available = get(&components, out);
        available->out[available->nout++] = (struct Connection){ out, in, id };
        id <<= 1;
    }
    fclose(f);
    printf("Part 1: %ld\n", best_path(0, components, 0).strength);
    printf("Part 2: %ld\n", longest_path(0, components, 0).strength);
    return 0;
}
