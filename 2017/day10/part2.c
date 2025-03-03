#include "hash.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLEN 100

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
    fgets(s, MAXLEN, f);
    size_t len = strlen(s);
    if (s[len - 1] == '\n') {
        s[len - 1] = '\0';  // Trim newline.
    }
    fclose(f);

    char * c = s;
    char ks[MAXLEN] = { 0 };
    size_t nks = 0;
    while (*c != '\0') {
        ks[nks++] = (char)*c++;
    }
    uint8_t h[HASH_ELEMS] = { 0 };
    hash(h, ks, nks);
    char hex[HASH_ELEMS + 1];
    tohex(hex, h);
    printf("%s\n", hex);
    return 0;
}
