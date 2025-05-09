#include "particle.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define LOG_IMPL
#include "/home/robin/src/clib/logging/log.h"
enum LogLevel LOG_LEVEL = LOG_INFO;

#define MAXLEN 1000

void
log_particles(
    enum LogLevel const level, struct Particle * particles, size_t const n
)
{
    char line[MAXLEN * MAXLEN] = { "\n" };
    size_t sz = 1;

    for (size_t i = 0; i < n; ++i) {
        sz += format_particle(line + sz, particles[i]);
        sz += sprintf(line + sz, "\n");
    }
    LOG(level, "%s", line);
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

    np = remove_collisions(particles, np);
    for (size_t iter = 0; iter < 1000; iter++) {
        LOG(LOG_DEBUG, "%zu: Moving %zu particles\n", iter, np);
        for (size_t i = 0; i < np; ++i) {
            particles[i] = move(particles[i]);
        }
        size_t new_np = remove_collisions2(particles, np);
        if (np != new_np) {
            LOG(LOG_INFO, "Found overlaps at iter %zu, from %zu to %zu\n", iter,
                np, new_np);
        }
        np = new_np;
    }

    printf("Part 2: %zu\n", np);
    return 0;
}
