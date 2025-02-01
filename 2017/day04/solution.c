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

struct Validation {
    bool part1;
    bool part2;
};

bool
anagram(char const * s1, char const * s2)
{
    size_t n1[26] = { 0 };
    size_t n2[26] = { 0 };
    while (*s1 != '\0') {
        n1[*s1++ - 'a']++;
    }
    while (*s2 != '\0') {
        n2[*s2++ - 'a']++;
    }
    for (size_t i = 0; i < 26; ++i) {
        if (n1[i] != n2[i]) {
            return false;
        }
    }
    return true;
}

struct Validation
is_valid(char * s)
{
    char ** parts = malloc(MAXSPLITS * sizeof(char *));
    struct StrSet *t1, *t2;
    struct Validation valid = {true, true};
    for (size_t i = 0; i < MAXSPLITS; ++i) {
        parts[i] = malloc(MAXLEN);
    }
    size_t n = strnsplit(parts, s, " ", MAXSPLITS, MAXLEN);
    struct StrSet * enc = NULL;
    struct StrSet * r = NULL;
    for (size_t i = 0; i < n; ++i) {
        HASH_FIND_STR(enc, parts[i], r);
        if (r) {
            valid.part1 = false;
            valid.part2 = false;
            goto cleanup;
        }
        struct StrSet * tmp;
        HASH_ITER(hh, enc, r, tmp) {
            if (anagram(parts[i], r->s)) {
                valid.part2 = false;
                break;
            }
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

    int valid1 = 0;
    int valid2 = 0;
    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0'; // Trim newline
        struct Validation v = is_valid(s);
        valid1 += v.part1;
        valid2 += v.part2;
    }
    fclose(f);
    free(s);
    printf("Part 1: %d\nPart 2: %d\n", valid1, valid2);
}
