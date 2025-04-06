#include "/home/robin/src/clib/test/minunit.h"
#include "particle.h"
#include <stdbool.h>
#include <string.h>

char BUF[1000];

#define mu_test_particle_eq(msg, want, got)                                   \
    do {                                                                      \
        mu_test_equal("", want.idx, got.idx, MU_NO_CLEANUP);                  \
        sprintf(BUF + 50, "%s (Pos)", msg);                                   \
        mu_test(BUF + 50, V3_eq(want.pos, got.pos), MU_NO_CLEANUP);           \
        sprintf(BUF + 50, "%s (Vel)", msg);                                   \
        mu_test(BUF + 50, V3_eq(want.vel, got.vel), MU_NO_CLEANUP);           \
        sprintf(BUF + 50, "%s (Acc)", msg);                                   \
        mu_test(BUF + 50, V3_eq(want.acc, got.acc), MU_NO_CLEANUP);           \
    } while (0)

#define mu_test_particles_eq(msg, want, got, n_want, n_got)                   \
    do {                                                                      \
        mu_test_equal(" ns", n_want, n_got, MU_NO_CLEANUP);                   \
        for (size_t __i = 0; __i < n_want; ++__i) {                           \
            sprintf(BUF, "%s: %zu", msg, __i);                                \
            mu_test_particle_eq(BUF, want[__i], got[__i]);                    \
        }                                                                     \
    } while (0)

char *
test_l1(void)
{
    mu_test_equal("", l1((struct V3){ 0, 0, 0 }, ORIGIN), 0, MU_NO_CLEANUP);
    mu_test_equal("", l1((struct V3){ 1, 2, 3 }, ORIGIN), 6, MU_NO_CLEANUP);
    mu_test_equal("", l1((struct V3){ 1, -2, -3 }, ORIGIN), 6, MU_NO_CLEANUP);
    return NULL;
}

char *
test_V3_eq(void)
{
    struct V3 a = { 1, 2, 3 };
    mu_test("", V3_eq(a, (struct V3){ 1, 2, 3 }), MU_NO_CLEANUP);
    mu_test("", !V3_eq(a, (struct V3){ 2, 2, 3 }), MU_NO_CLEANUP);
    mu_test("", !V3_eq(a, (struct V3){ -1, -2, -3 }), MU_NO_CLEANUP);
    return NULL;
}

char *
test_parse(void)
{
    char * s = "p=<1,2,3>, v=<-4,-5,-6>, a=<1000, 2000, 3000>";
    struct Particle parsed = parse_particle(s, 8);
    struct Particle want = {
        .idx = 8,
        .pos = { 1, 2, 3 },
        .vel = { -4, -5, -6 },
        .acc = { 1000, 2000, 3000 },
    };
    mu_test_particle_eq("", want, parsed);
    return NULL;
}

char *
test_move(void)
{
    struct Particle p = { .pos = { 0, 1, 2 },
                          .vel = { 10, 20, 30 },
                          .acc = { 100, 200, 300 } };
    struct Particle got = move(p);
    struct Particle want = { .pos = { 110, 221, 332 },
                             .vel = { 110, 220, 330 },
                             .acc = { 100, 200, 300 } };
    mu_test_particle_eq("", want, got);
    return NULL;
}

char *
test_V3_add(void)
{
    mu_test(
        "",
        V3_eq(
            V3_add((struct V3){ 1, 2, 3 }, (struct V3){ 10, 20, 30 }),
            (struct V3){ 11, 22, 33 }
        ),
        MU_NO_CLEANUP
    );
    return NULL;
}

char *
test_l1_difference(void)
{
    struct Particle a = { .pos = { 0, 0, 0 } };
    struct Particle b = { .pos = { 1, 2, 3 } };
    struct Particle c = { .pos = { 1, -2, 3 } };
    mu_test_equal("", 0, l1_difference(&a, &a), MU_NO_CLEANUP);
    mu_test_equal("", -6, l1_difference(&a, &b), MU_NO_CLEANUP);
    mu_test_equal("", 6, l1_difference(&b, &a), MU_NO_CLEANUP);
    mu_test_equal("", 0, l1_difference(&b, &c), MU_NO_CLEANUP);
    return NULL;
}

char *
test_particle_sort(void)
{
    struct Particle a = { .pos = { 0, 0, 0 } };
    struct Particle b = { .pos = { 0, 0, 1 } };
    struct Particle c = { .pos = { 0, 1, 1 } };
    struct Particle d = { .pos = { 1, 1, 1 } };
    mu_test_equal("", 0, particle_sort(&a, &a), MU_NO_CLEANUP);
    mu_test_equal("", 0, particle_sort(&b, &b), MU_NO_CLEANUP);
    mu_test_equal("", -1, particle_sort(&a, &b), MU_NO_CLEANUP);
    mu_test_equal("", -2, particle_sort(&a, &c), MU_NO_CLEANUP);
    mu_test_equal("", -3, particle_sort(&a, &d), MU_NO_CLEANUP);
    mu_test_equal("", -1, particle_sort(&b, &c), MU_NO_CLEANUP);
    mu_test_equal("", -2, particle_sort(&b, &d), MU_NO_CLEANUP);
    mu_test_equal("", -1, particle_sort(&c, &d), MU_NO_CLEANUP);

    mu_test_equal("", 1, particle_sort(&b, &a), MU_NO_CLEANUP);
    mu_test_equal("", 2, particle_sort(&c, &a), MU_NO_CLEANUP);
    mu_test_equal("", 3, particle_sort(&d, &a), MU_NO_CLEANUP);
    mu_test_equal("", 1, particle_sort(&c, &b), MU_NO_CLEANUP);
    mu_test_equal("", 2, particle_sort(&d, &b), MU_NO_CLEANUP);
    mu_test_equal("", 1, particle_sort(&d, &c), MU_NO_CLEANUP);
    return NULL;
}

char *
test_remove_collisions(void)
{
    struct Particle particles[10];
    struct Particle want[10];
    size_t n;

    memset(particles, 0, 10 * sizeof(*particles));
    particles[0].pos = (struct V3){ 3, 0, 0 };
    particles[1].pos = (struct V3){ 0, 0, 0 };
    particles[2].pos = (struct V3){ 1, 0, 0 };
    particles[3].pos = (struct V3){ 2, 0, 0 };
    particles[4].pos = (struct V3){ 4, 0, 0 };
    memset(want, 0, 10 * sizeof(*particles));
    want[0].pos = (struct V3){ 0, 0, 0 };
    want[1].pos = (struct V3){ 1, 0, 0 };
    want[2].pos = (struct V3){ 2, 0, 0 };
    want[3].pos = (struct V3){ 3, 0, 0 };
    want[4].pos = (struct V3){ 4, 0, 0 };
    n = remove_collisions(particles, 5);
    mu_test_particles_eq("No duplicates", want, particles, 5, n);

    memset(particles, 0, 10 * sizeof(*particles));
    particles[0].pos = (struct V3){ 1, 0, 0 };
    particles[1].pos = (struct V3){ 1, 0, 0 };
    particles[2].pos = (struct V3){ 2, 0, 0 };
    particles[3].pos = (struct V3){ 3, 0, 0 };
    particles[4].pos = (struct V3){ 4, 0, 0 };
    memset(want, 0, 10 * sizeof(*particles));
    want[0].pos = (struct V3){ 2, 0, 0 };
    want[1].pos = (struct V3){ 3, 0, 0 };
    want[2].pos = (struct V3){ 4, 0, 0 };
    n = remove_collisions(particles, 5);
    mu_test_particles_eq("Dupes at beginning", want, particles, 3, n);

    memset(particles, 0, 10 * sizeof(*particles));
    particles[0].pos = (struct V3){ 1, 0, 0 };
    particles[1].pos = (struct V3){ 1, 0, 0 };
    particles[2].pos = (struct V3){ 1, 1, 0 };
    particles[3].pos = (struct V3){ 1, 1, 0 };
    particles[4].pos = (struct V3){ 4, 0, 0 };
    memset(want, 0, 10 * sizeof(*particles));
    want[0].pos = (struct V3){ 4, 0, 0 };
    n = remove_collisions(particles, 5);
    mu_test_particles_eq("Many dupes at beginning", want, particles, 1, n);

    particles[0].pos = (struct V3){ 0, 0, 0 };
    particles[1].pos = (struct V3){ 0, 0, 0 };
    particles[2].pos = (struct V3){ 0, 0, 0 };
    particles[3].pos = (struct V3){ 0, 0, 0 };
    particles[4].pos = (struct V3){ 0, 0, 0 };
    n = remove_collisions(particles, 5);
    mu_test_particles_eq("All dupes", want, particles, 0, n);

    memset(particles, 0, 10 * sizeof(*particles));
    particles[0].pos = (struct V3){ 3, 0, 0 };
    particles[1].pos = (struct V3){ 0, 0, 0 };
    particles[2].pos = (struct V3){ 1, 0, 0 };
    particles[3].pos = (struct V3){ 4, 0, 0 };
    particles[4].pos = (struct V3){ 4, 0, 0 };
    memset(want, 0, 10 * sizeof(*particles));
    want[0].pos = (struct V3){ 0, 0, 0 };
    want[1].pos = (struct V3){ 1, 0, 0 };
    want[2].pos = (struct V3){ 3, 0, 0 };
    n = remove_collisions(particles, 5);
    mu_test_particles_eq("Dupes at end", want, particles, 3, n);

    memset(particles, 0, 10 * sizeof(*particles));
    particles[0].pos = (struct V3){ 3, 0, 0 };
    particles[1].pos = (struct V3){ 0, 0, 0 };
    particles[2].pos = (struct V3){ 4, 0, 0 };
    particles[3].pos = (struct V3){ 4, 0, 0 };
    particles[4].pos = (struct V3){ 4, 0, 0 };
    memset(want, 0, 10 * sizeof(*particles));
    want[0].pos = (struct V3){ 0, 0, 0 };
    want[1].pos = (struct V3){ 3, 0, 0 };
    n = remove_collisions(particles, 5);
    mu_test_particles_eq("Many dupes at end", want, particles, 2, n);

    memset(particles, 0, 10 * sizeof(*particles));
    particles[0].pos = (struct V3){ 0, 0, 0 };
    particles[1].pos = (struct V3){ 1, 0, 0 };
    particles[2].pos = (struct V3){ 2, 0, 0 };
    particles[3].pos = (struct V3){ 2, 0, 0 };
    particles[4].pos = (struct V3){ 4, 0, 0 };
    memset(want, 0, 10 * sizeof(*particles));
    want[0].pos = (struct V3){ 0, 0, 0 };
    want[1].pos = (struct V3){ 1, 0, 0 };
    want[2].pos = (struct V3){ 4, 0, 0 };
    format_particle(BUF + 100, particles[1]);
    n = remove_collisions(particles, 5);
    mu_test_particles_eq("Dupes in middle", want, particles, 3, n);

    memset(particles, 0, 10 * sizeof(*particles));
    particles[0].pos = (struct V3){ 0, 0, 0 };
    particles[1].pos = (struct V3){ 2, 0, 0 };
    particles[2].pos = (struct V3){ 2, 0, 0 };
    particles[3].pos = (struct V3){ 2, 0, 0 };
    particles[4].pos = (struct V3){ 4, 0, 0 };
    memset(want, 0, 10 * sizeof(*particles));
    want[0].pos = (struct V3){ 0, 0, 0 };
    want[1].pos = (struct V3){ 4, 0, 0 };
    n = remove_collisions(particles, 5);
    mu_test_particles_eq("Many Dupes in middle", want, particles, 2, n);

    memset(particles, 0, 10 * sizeof(*particles));
    particles[0].pos = (struct V3){ 0, 0, 0 };
    particles[1].pos = (struct V3){ 1, 0, 0 };
    particles[2].pos = (struct V3){ 1, 0, 0 };
    particles[3].pos = (struct V3){ 2, 0, 0 };
    particles[4].pos = (struct V3){ 3, 0, 0 };
    particles[5].pos = (struct V3){ 3, 0, 0 };
    particles[6].pos = (struct V3){ 3, 0, 0 };
    particles[7].pos = (struct V3){ 4, 0, 0 };
    particles[8].pos = (struct V3){ 5, 0, 0 };
    particles[9].pos = (struct V3){ 5, 0, 0 };
    memset(want, 0, 10 * sizeof(*particles));
    want[0].pos = (struct V3){ 0, 0, 0 };
    want[1].pos = (struct V3){ 2, 0, 0 };
    want[2].pos = (struct V3){ 4, 0, 0 };
    n = remove_collisions(particles, 10);
    mu_test_particles_eq("Many sets of Dupes", want, particles, 3, n);
    return NULL;
}

char *
all_tests(void)
{
    mu_run_test(test_l1);
    mu_run_test(test_V3_eq);
    mu_run_test(test_parse);
    mu_run_test(test_move);
    mu_run_test(test_V3_add);
    mu_run_test(test_l1_difference);
    mu_run_test(test_particle_sort);
    mu_run_test(test_remove_collisions);
    return NULL;
}

int
main(void)
{
    mu_main(all_tests);
    return tests_failed;
}
