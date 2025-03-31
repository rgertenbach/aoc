#include "/home/robin/src/clib/test/minunit.h"
#include "particle.h"
#include <stdbool.h>

#define mu_test_particle_eq(msg, want, got)                                   \
    do {                                                                      \
        mu_test_equal(msg, want.idx, got.idx, MU_NO_CLEANUP);                 \
        mu_test(msg, V3_eq(want.pos, got.pos), MU_NO_CLEANUP);                \
        mu_test(msg, V3_eq(want.vel, got.vel), MU_NO_CLEANUP);                \
        mu_test(msg, V3_eq(want.acc, got.acc), MU_NO_CLEANUP);                \
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
    struct Particle a = {.pos = {0, 0, 0}};
    struct Particle b = {.pos = {1, 2, 3}};
    struct Particle c = {.pos = {1, -2, 3}};
    mu_test_equal("", 0, l1_difference(&a, &a), MU_NO_CLEANUP);
    mu_test_equal("", -6, l1_difference(&a, &b), MU_NO_CLEANUP);
    mu_test_equal("", 6, l1_difference(&b, &a), MU_NO_CLEANUP);
    mu_test_equal("", 0, l1_difference(&b, &c), MU_NO_CLEANUP);
    return NULL;
}

char *
test_particle_sort(void)
{
    struct Particle a = {.pos = {0, 0, 0}};
    struct Particle b = {.pos = {0, 0, 1}};
    struct Particle c = {.pos = {0, 1, 1}};
    struct Particle d = {.pos = {1, 1, 1}};
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
all_tests(void)
{
    mu_run_test(test_l1);
    mu_run_test(test_V3_eq);
    mu_run_test(test_parse);
    mu_run_test(test_move);
    mu_run_test(test_V3_add);
    mu_run_test(test_l1_difference);
    mu_run_test(test_particle_sort);
    return NULL;
}

int
main(void)
{
    mu_main(all_tests);
}
