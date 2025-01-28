#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "/home/robin/src/clib/string/str.h"

#define MAXLEN 10000

int32_t
captcha(char const * const s)
{
    int32_t out = 0;
    size_t n = strlen(s);
    for (size_t i = 0; i < n; ++i) {
        if (s[i] == s[(i + n / 2) % n]) {
            out += s[i] - '0';
        }
    }
    return out;
}

int
main(int const argc, char const * const * const argv)
{
    if (argc < 2) {
        fprintf(stderr, "No input filename provided\n");
        return 1;
    }
    FILE * file = fopen(argv[1], "r");
    if (file == NULL) {
        fprintf(stderr, "Could not open file.\n");
        return 2;
    }
    char * s = malloc(MAXLEN);
    fgets(s, MAXLEN, file);
    str_rstrip(s, "\n");
    fclose(file);

    printf("%d\n", captcha(s));
    return 0;
}
