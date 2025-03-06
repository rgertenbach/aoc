#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 2017

int main(int const argc, char const * const * const argv)
{
    if (argc < 2) {
        fprintf(stderr, "Need to supply input\n");
        exit(1);
    }
    ptrdiff_t jump = atoi(argv[1]);
    int arr[N + 1] = {0};
    size_t sz = 1;
    size_t p = 0;
    for (size_t i = 0; i < N; ++i) {
        p = (p + jump) % sz;
        memmove(arr + p + 2, arr + p + 1, sizeof(*arr) * (sz - p - 1));
        arr[++p] = i + 1;
        sz++;

    }
    printf("Part 1: %d\n", arr[(p + 1) % sz]);

    return 0;
}
