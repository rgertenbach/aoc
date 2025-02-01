#include "/home/robin/src/clib/string/split.h"
#include "uthash.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define MAXSPLITS 100
#define MAXLEN 1000

struct StrSet {
    char s[MAXLEN];
    UT_hash_handle hh;
};

bool
is_valid(char * s)
{
    char ** parts = malloc(MAXSPLITS * sizeof(char *));
    struct StrSet *t1, *t2;
    bool valid = true;
    for (size_t i = 0; i < MAXSPLITS; ++i) {
        parts[i] = malloc(MAXLEN);
    }
    size_t n = strnsplit(parts, s, " ", MAXSPLITS, MAXLEN);
    struct StrSet * enc = NULL;
    struct StrSet * r = NULL;
    for (size_t i = 0; i < n; ++i) {
        HASH_FIND_STR(enc, parts[i], r);
        if (r) {
            valid = false;
            goto cleanup;
        }
        r = malloc(sizeof(struct StrSet));
        strcpy(r->s, parts[i]);
        HASH_ADD_STR(enc, s, r);
    }
cleanup:
    HASH_ITER(hh, enc, t1, t2)
    {
        HASH_DEL(enc, t1);
        free(t1);
    }
    return valid;
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
    char * s = malloc(MAXLEN);

    int valid = 0;
    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline
        valid += is_valid(s);
    }
    fclose(f);
    free(s);
    printf("%d\n", valid);
}
