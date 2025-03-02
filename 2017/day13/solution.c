#include "firewall.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLEN 1000

void
add_layer(struct Firewall ** fw, char const * line)
{
    size_t layer = 0;
    size_t range = 0;
    bool in_range = false;
    while (*line != '\0') {
        if (*line == ':') {
            in_range = true;
            line++;
        } else if (in_range) {
            range *= 10;
            range += *line - '0';
        } else {
            layer *= 10;
            layer += *line - '0';
        }
        line++;
    }
    fw_add(fw, layer, range);
}

bool gets_caught(struct Firewall * fw, size_t const delay)
{
    struct Firewall *c, *n;
    HASH_ITER(hh, fw, c, n)
    {
        if (pos_steps_from_now(c, delay + c->layer) == 0) {
            return true;
        }
    }
    return false;
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

    struct Firewall * fw = NULL;
    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        add_layer(&fw, s);
    }
    fclose(f);

    size_t part1 = 0;
    struct Firewall *c, *n;
    HASH_ITER(hh, fw, c, n)
    {
        if (pos_steps_from_now(c, c->layer) == 0) {
            part1 += c->layer * c->range;
        }
    }

    printf("Part 1: %zu\n", part1);

    size_t delay = 0;
    while (gets_caught(fw, delay)) {
        delay++;
    }
    printf("Part 2: %zu\n", delay);
    return 0;
}
