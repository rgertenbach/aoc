#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N1 2017
#define N2 50000000

int
part1(ptrdiff_t const jump)
{
    int arr[N1 + 1] = { 0 };
    size_t sz = 1;
    size_t p = 0;
    for (size_t i = 0; i < N1; ++i) {
        p = (p + jump) % sz;
        memmove(arr + p + 2, arr + p + 1, sizeof(*arr) * (sz - p - 1));
        arr[++p] = i + 1;
        sz++;
    }
    return arr[(p + 1) % sz];
}

int
part2(ptrdiff_t const jump)
{
    size_t i = 1;
    size_t p = 1;
    int after0 = 1;
    while (i++ < N2) {
        p = (p + jump) % i + 1;
        if (p == 1) {after0 = i;}
    }
    return after0;
}

int
main(int const argc, char const * const * const argv)
{
    if (argc < 2) {
        fprintf(stderr, "Need to supply input\n");
        exit(1);
    }
    ptrdiff_t jump = atoi(argv[1]);
    printf("Part 1: %d\n", part1(jump));
    printf("Part 2: %d\n", part2(jump));

    return 0;
}
