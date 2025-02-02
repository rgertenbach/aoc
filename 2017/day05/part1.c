#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLEN 2000

int main(int const argc, char const * const * const argv)
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
    char * s = malloc(MAXLEN);
    int jumps[MAXLEN];
    size_t n = 0;

    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        sscanf(s, "%d", jumps + (n++));
    }
    fclose(f);
    size_t p = 0;
    size_t steps = 0;
    while (p < n) {
        jumps[p]++;
        p += jumps[p] - 1;
        steps++;
    }
    printf("%zu\n", steps);
}
