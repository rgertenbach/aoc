#include "particle.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define LOG_IMPL
#include "/home/robin/src/clib/logging/log.h"
enum LogLevel LOG_LEVEL = LOG_WARN;

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
    struct Particle particles[MAXLEN];
    size_t np = 0;
    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        particles[np] = parse_particle(s, np);
        np++;
    }
    fclose(f);

    for (size_t iter = 0; iter < 1000; iter++) {
        LOG(LOG_DEBUG, "%zu: Moving %zu particles\n", iter, np);
        for (size_t i = 0; i < np; ++i) {
            particles[i] = move(particles[i]);
        }
    }

    int64_t min_dist = INT64_MAX;
    size_t which_min = SIZE_MAX;

    for (size_t i = 0; i < np; i++) {
        int64_t d = l1(particles[i].pos, ORIGIN);
        if (d < min_dist) {
            min_dist = d;
            which_min = i;
        }
    }

    printf("Part 1: %zu\n", which_min);
    return 0;
}
