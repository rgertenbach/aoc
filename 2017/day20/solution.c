#include "particle.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLEN 1000

size_t remove_collisions(struct Particle * particles, size_t n)
{
    qsort(particles, n, sizeof(*particles), l1_difference);
    size_t left = 0, right = 0;
    size_t n_same = 0;
    for (; right < n; ++right) {

    }
    return left + right + n_same;
    return n;
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
    struct Particle particles[MAXLEN];
    size_t np = 0;
    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        particles[np] = parse_particle(s, np);
        np++;
    }
    fclose(f);

    for (size_t iter = 0; iter < 1000; iter++) {
        for (size_t i = 0; i < np; ++i) {
            particles[i] = move(particles[i]);
        }
        np = remove_collisions(particles, np);
    }
    printf("Part 1: %zu\n", particles[0].idx);
    return 0;
}
