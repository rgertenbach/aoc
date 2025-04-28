#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <uthash.h>

#define MAXLEN 1000

enum Move { MOVE_LEFT = 0, MOVE_RIGHT = 1 };

struct Steps {
    char write;
    enum Move move;
    char new_state;
};

struct Operation {
    char state;
    struct Steps if0;
    struct Steps if1;
};

struct Tape {
    UT_hash_handle hh;
    int64_t pos;
    char val;
};

struct Tape *
get(struct Tape ** tape, int64_t const pos)
{
    struct Tape * f = NULL;
    HASH_FIND(hh, *tape, &pos, sizeof(pos), f);
    if (f == NULL) {
        f = malloc(sizeof(struct Tape));
        f->pos = pos;
        f->val = 0;
        HASH_ADD(hh, *tape, pos, sizeof(pos), f);
    }
    return f;
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
    char s[MAXLEN];
    fgets(s, MAXLEN, f);
    char current_state = s[strlen(s) - 3];
    fgets(s, MAXLEN, f);
    size_t nsteps;
    sscanf(s, "Perform a diagnostic checksum after %zu", &nsteps);
    struct Operation ops[6];
    fgets(s, MAXLEN, f);  // Skip blank line
    struct Tape * tape = NULL;
    while (fgets(s, MAXLEN, f)) {
        struct Operation op;
        op.state = s[9];

        fgets(s, MAXLEN, f);  // If current value is 0:
        op.if0.write = fgets(s, MAXLEN, f)[22] - '0';
        op.if0.move = (fgets(s, MAXLEN, f)[27] == 'l' ? MOVE_LEFT : MOVE_RIGHT);
        op.if0.new_state = fgets(s, MAXLEN, f)[26];  // Continue with State x

        fgets(s, MAXLEN, f);  // If current value is 1:
        op.if1.write = fgets(s, MAXLEN, f)[22] - '0';
        op.if1.move = (fgets(s, MAXLEN, f)[27] == 'l' ? MOVE_LEFT : MOVE_RIGHT);
        op.if1.new_state = fgets(s, MAXLEN, f)[26];  // Continue with State x
        fgets(s, MAXLEN, f);  // Skip blank line

        ops[op.state - 'A'] = op;
    }
    fclose(f);

    int64_t pos = 0;
    for (size_t i = 0; i < nsteps; ++i) {
        struct Tape * t = get(&tape, pos);
        struct Operation op = ops[current_state - 'A'];
        if (t->val) {  // 1
            t->val = op.if1.write;
            pos += (op.if1.move == MOVE_LEFT ? -1 : 1);
            current_state = op.if1.new_state;
        } else {  // 0
            t->val = op.if0.write;
            pos += (op.if0.move == MOVE_LEFT ? -1 : 1);
            current_state = op.if0.new_state;
        }
    }
    int64_t checksum = 0;
    struct Tape *t, *n;
    HASH_ITER(hh, tape, t, n)
    {
        checksum += t->val;
    }
    printf("Part 1: %ld\n", checksum);
    return 0;
}
