#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "/home/robin/src/clib/string/str.h"

#define MAXLEN 10000

int32_t
captcha(char const * const s)
{
    int32_t out = 0;
    char const * p = s;
    while (*(++p) != '\0') {
        if (*p == *(p - 1)) {
            out += *p - '0';
        }
    }
    if (*(--p) == *s) {
        out += *s - '0';
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
