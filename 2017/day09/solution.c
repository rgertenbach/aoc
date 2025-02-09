#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXLEN 50000

struct Points {
    int part1;
    int part2;
};

struct Points
parse(char const * s)
{
    struct Points p = {0, 0};
    int depth = 1;
    s++;
    bool garbage = false;
    while (*s != '\0') {
        if (garbage) {
            switch (*s) {
            case '!':
                s++;
                break;
            case '>':
                garbage = false;
                break;
            default:
                p.part2++;
                break;
            }
        } else {
            switch (*s) {
            case '<':
                garbage = true;
                true;
                break;
            case '{':
                depth++;
                break;
            case '}':
                p.part1 += depth;
                depth--;
                break;
            }
        }
        s++;
    }
    return p;
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

    fgets(s, MAXLEN, f);
    s[strlen(s) - 1] = '\0';  // Trim newline.
    fclose(f);
    struct Points p = parse(s);
    printf("Part 1: %d\nPart 2: %d\n", p.part1, p.part2);
    return 0;
}
