#include "/home/robin/src/clib/test/minunit.h"
#include "automaton.h"
#include <string.h>

char buf[1000];

#define mu_pattern_eq(p1, p2)                                                 \
    do {                                                                      \
        mu_test_equal("Strides Match", p1.stride, p2.stride, MU_NO_CLEANUP);  \
        mu_test(                                                              \
            "Pattern match",                                                  \
            !strncmp(p1.pattern, p2.pattern, p1.stride * p1.stride),          \
            MU_NO_CLEANUP                                                     \
        );                                                                    \
    } while (0)

#define mu_replacement_eq(r1, r2)                                             \
    do {                                                                      \
        mu_pattern_eq(r1.match, r2.match);                                    \
        mu_pattern_eq(r1.replacement, r2.replacement);                        \
    } while (0)

char *
test_parse_replacement(void)
{
    char * s = "#./#. => #../#../#..";
    struct Replacement got = parse_replacement(s);
    struct Replacement want = {
        .match = { .stride = 2, .pattern = "#.#." },
        .replacement = { .stride = 3, .pattern = "#..#..#.." },
    };
    format_pattern(buf, got.match);
    mu_replacement_eq(got, want);
    return NULL;
}

char *
test_pattern_at(void)
{
    Grid_t grid;
    strcpy(grid[0], "#.0000");
    strcpy(grid[1], "#.1111");
    strcpy(grid[2], "##2222");
    strcpy(grid[3], "##3333");
    struct Pattern got = pattern_at(0, 0, grid, 2);
    struct Pattern want = { .pattern = "#.#.", .stride = 2 };
    mu_pattern_eq(got, want);
    return NULL;
}

char *
test_rotate_pattern(void)
{
    struct Pattern want;
    struct Pattern got = { .stride = 2, .pattern = "1234" };
    got = rotate_pattern(got);
    want = (struct Pattern){ .stride = 2, .pattern = "3142" };
    mu_pattern_eq(want, got);

    got = rotate_pattern(got);
    want = (struct Pattern){ .stride = 2, .pattern = "4321" };
    mu_pattern_eq(want, got);

    got = rotate_pattern(got);
    want = (struct Pattern){ .stride = 2, .pattern = "2413" };
    mu_pattern_eq(want, got);

    got = (struct Pattern){ .stride = 3, .pattern = "123456789" };
    got = rotate_pattern(got);
    want = (struct Pattern){ .stride = 3, .pattern = "741852963" };
    mu_pattern_eq(want, got);

    got = rotate_pattern(got);
    want = (struct Pattern){ .stride = 3, .pattern = "987654321" };
    mu_pattern_eq(want, got);

    got = rotate_pattern(got);
    want = (struct Pattern){ .stride = 3, .pattern = "369258147" };
    mu_pattern_eq(want, got);

    return NULL;
}

char *
test_hflip_pattern(void)
{
    struct Pattern want, got, input;
    input = (struct Pattern){ .stride = 2, .pattern = "1234" };
    got = hflip_pattern(input);
    want = (struct Pattern){ .stride = 2, .pattern = "3412" };
    mu_pattern_eq(want, got);

    input = (struct Pattern){ .stride = 3, .pattern = "123456789" };
    got = hflip_pattern(input);
    want = (struct Pattern){ .stride = 3, .pattern = "789456123" };
    mu_pattern_eq(want, got);
    return NULL;
}

char *
test_vflip_pattern(void)
{
    struct Pattern want, got, input;
    input = (struct Pattern){ .stride = 2, .pattern = "1234" };
    got = vflip_pattern(input);
    want = (struct Pattern){ .stride = 2, .pattern = "2143" };
    mu_pattern_eq(want, got);

    input = (struct Pattern){ .stride = 3, .pattern = "123456789" };
    got = vflip_pattern(input);
    want = (struct Pattern){ .stride = 3, .pattern = "321654987" };
    mu_pattern_eq(want, got);
    return NULL;
}

char *
test_patterns_match(void)
{
    struct Pattern input, other;
    other = (struct Pattern){ .stride = 2, .pattern = "###." };

    input = (struct Pattern){ .stride = 2, .pattern = "###." };
    mu_test("2 0", patterns_match(input, other), MU_NO_CLEANUP);
    input = (struct Pattern){ .stride = 2, .pattern = "##.#" };
    mu_test("2 1", patterns_match(input, other), MU_NO_CLEANUP);
    input = (struct Pattern){ .stride = 2, .pattern = "#.##" };
    mu_test("2 2", patterns_match(input, other), MU_NO_CLEANUP);
    input = (struct Pattern){ .stride = 2, .pattern = ".###" };
    mu_test("2 3", patterns_match(input, other), MU_NO_CLEANUP);
    input = (struct Pattern){ .stride = 2, .pattern = "####" };
    mu_test("2 x", !patterns_match(input, other), MU_NO_CLEANUP);

    other = (struct Pattern){ .stride = 3, .pattern = "########." };

    input = (struct Pattern){ .stride = 3, .pattern = "########." };
    mu_test("3 0", patterns_match(input, other), MU_NO_CLEANUP);
    input = (struct Pattern){ .stride = 3, .pattern = "#######.#" };
    mu_test("3 1", !patterns_match(input, other), MU_NO_CLEANUP);
    input = (struct Pattern){ .stride = 3, .pattern = "######.##" };
    mu_test("3 2", patterns_match(input, other), MU_NO_CLEANUP);
    input = (struct Pattern){ .stride = 3, .pattern = "#####.###" };
    mu_test("3 3", !patterns_match(input, other), MU_NO_CLEANUP);
    input = (struct Pattern){ .stride = 3, .pattern = "####.####" };
    mu_test("3 4", !patterns_match(input, other), MU_NO_CLEANUP);
    input = (struct Pattern){ .stride = 3, .pattern = "###.#####" };
    mu_test("3 5", !patterns_match(input, other), MU_NO_CLEANUP);
    input = (struct Pattern){ .stride = 3, .pattern = "##.######" };
    mu_test("3 6", patterns_match(input, other), MU_NO_CLEANUP);
    input = (struct Pattern){ .stride = 3, .pattern = "#.#######" };
    mu_test("3 7", !patterns_match(input, other), MU_NO_CLEANUP);
    input = (struct Pattern){ .stride = 3, .pattern = ".########" };
    mu_test("3 8", patterns_match(input, other), MU_NO_CLEANUP);
    input = (struct Pattern){ .stride = 3, .pattern = "#########" };
    mu_test("3 x", !patterns_match(input, other), MU_NO_CLEANUP);
    return NULL;
}

char *
test_find_replacement(void)
{
    struct Replacement patterns[] = {
        { .match = { .stride = 2, .pattern = "###." },
          .replacement = { .stride = 3, .pattern = "########." } },
        { .match = { .stride = 2, .pattern = "##.." },
          .replacement = { .stride = 3, .pattern = "########." } },
        { .match = { .stride = 2, .pattern = "#..." },
          .replacement = { .stride = 3, .pattern = "........." } },
    };
    struct Pattern input = { .stride = 2, .pattern = "...#" };
    struct Pattern got = find_replacement(input, patterns, 3);
    struct Pattern want = { .stride = 3, .pattern = "........." };
    mu_pattern_eq(got, want);
    return NULL;
}

char *
test_grow(void)
{
    Grid_t grid = { ".#", ".." };
    size_t grid_sz = 2;
    Grid_t got;

    // ..     ...      ....
    // .#  -> ...  ->  .#.#
    //        ..#      ....
    //                 .#.#
    struct Replacement patterns[] = {
        { .match = { .stride = 2,
                     .pattern = ".."
                                ".#" },
          .replacement = { .stride = 3,
                           .pattern = "..."
                                      "..."
                                      "..#" } },
        { .match = { .stride = 3,
                     .pattern = "..."
                                "..."
                                "..#" },
          .replacement = { .stride = 4,
                           .pattern = "...."
                                      ".#.#"
                                      "...."
                                      ".#.#" } },
    };

    grid_sz = grow(got, grid, grid_sz, patterns, 2);
    mu_test_equal("2->3 Size", grid_sz, 3, MU_NO_CLEANUP);
    mu_test("2->3 row 0", !strncmp(got[0], "...", 3), MU_NO_CLEANUP);
    mu_test("2->3 row 1", !strncmp(got[1], "...", 3), MU_NO_CLEANUP);
    mu_test("2->3 row 2", !strncmp(got[2], "..#", 3), MU_NO_CLEANUP);

    memcpy(grid, got, sizeof(Grid_t));
    grid_sz = grow(got, grid, grid_sz, patterns, 2);
    mu_test_equal("3->4 Size", grid_sz, 4, MU_NO_CLEANUP);
    mu_test("3->4 row 0", !strncmp(got[0], "....", 4), MU_NO_CLEANUP);
    mu_test("3->4 row 1", !strncmp(got[1], ".#.#", 4), MU_NO_CLEANUP);
    mu_test("3->4 row 2", !strncmp(got[2], "....", 4), MU_NO_CLEANUP);
    mu_test("3->4 row 3", !strncmp(got[3], ".#.#", 4), MU_NO_CLEANUP);

    memcpy(grid, got, sizeof(Grid_t));
    grid_sz = grow(got, grid, grid_sz, patterns, 2);
    mu_test_equal("4->6 Size", grid_sz, 6, MU_NO_CLEANUP);
    mu_test("4->6 row 0", !strncmp(got[0], "......", 6), MU_NO_CLEANUP);
    mu_test("4->6 row 1", !strncmp(got[1], "......", 6), MU_NO_CLEANUP);
    mu_test("4->6 row 2", !strncmp(got[2], "..#..#", 6), MU_NO_CLEANUP);
    mu_test("4->6 row 3", !strncmp(got[3], "......", 6), MU_NO_CLEANUP);
    mu_test("4->6 row 4", !strncmp(got[4], "......", 6), MU_NO_CLEANUP);
    mu_test("4->6 row 5", !strncmp(got[5], "..#..#", 6), MU_NO_CLEANUP);
    return NULL;
}

char *
run_all_tests(void)
{
    mu_run_test(test_parse_replacement);
    mu_run_test(test_pattern_at);
    mu_run_test(test_rotate_pattern);
    mu_run_test(test_hflip_pattern);
    mu_run_test(test_vflip_pattern);
    mu_run_test(test_patterns_match);
    mu_run_test(test_find_replacement);
    mu_run_test(test_grow);
    return NULL;
}

int
main(void)
{
    mu_main(run_all_tests);
    return tests_failed;
}
