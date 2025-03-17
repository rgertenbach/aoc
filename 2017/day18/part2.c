#include "part2.h"
#include "/home/robin/src/clib/logging/log.h"
#include "queue.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum LogLevel LOG_LEVEL = LOG_NOTHING;

#define MAXLEN 1000
char MSGBUF[MAXLEN];

char *
print_state(
    char * s,
    struct Result const state,
    size_t const pc,
    int64_t const * const registers,
    struct Queue const * signals
)
{
    char * current = s;
    current += sprintf(current, "|");
    switch (state.action) {
    case ACT_NIL:
        current += sprintf(current, "ACT_NIL ");
        break;
    case ACT_SND:
        current += sprintf(current, "ACT_SND ");
        break;
    case ACT_RCV:
        current += sprintf(current, "ACT_RCV ");
        break;
    case ACT_DED:
        current += sprintf(current, "ACT_DED ");
        break;
    }
    current += sprintf(current, "PC: %zu\n|", pc);
    for (char i = 'a'; i <= 'z'; ++i) {
        current += sprintf(current, "%10c", i);
    }
    current += sprintf(current, "\n|");
    for (size_t i = 0; i < 26; ++i) {
        current += sprintf(current, "%10ld", registers[i]);
    }
    current += sprintf(current, "\n");
    if (Queue_size(signals) == 0) {
        current += sprintf(current, "| # Signals: %zu", Queue_size(signals));
    } else {
        current += sprintf(
            current, "| # Signals: %zu with front %zu", Queue_size(signals),
            Queue_peek(signals)
        );
    }
    *current = '\0';
    return s;
}

int
main(int const argc, char const * const * const argv)
{
    if (argc < 2) {
        LOG(LOG_ERROR, "Need to supply filename\n");
        exit(1);
    }
    FILE * f = fopen(argv[1], "r");
    if (!f) {
        LOG(LOG_ERROR, "Could not open %s\n", argv[1]);
        exit(1);
    }
    char s[MAXLEN];

    struct Instruction instructions[100];
    size_t ninst = 0;
    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        instructions[ninst++] = parse(s);
    }
    fclose(f);

    int64_t registers0[DUET_REGISTER_SZ] = { 0 };
    int64_t registers1[DUET_REGISTER_SZ] = { 0 };
    struct Queue * signals0 = Queue_new();
    struct Queue * signals1 = Queue_new();

    registers1['p' - 'a'] = 1;
    size_t p0 = 0;
    size_t p1 = 0;
    struct Result r0 = { 0, ACT_NIL, 0 };
    struct Result r1 = { 0, ACT_NIL, 0 };

    char whoseturn = 0;
    size_t part2 = 0;
    while (can_process(r0, signals0) || can_process(r1, signals1)) {
        LOG(LOG_DEBUG, "\n\n");
        LOG(LOG_DEBUG, "Program 0:\n%s\n",
            print_state(MSGBUF, r0, p0, registers0, signals0));
        LOG(LOG_DEBUG, "Program 1:\n%s\n",
            print_state(MSGBUF, r1, p1, registers1, signals1));
        if (whoseturn == 0) {
            LOG(LOG_INFO, "Program 0's turn\n");
            r0 = op(registers0, instructions, ninst, p0, signals0);
            switch (r0.action) {
            case ACT_SND:
                Queue_append(signals1, r0.val);
                break;
            case ACT_RCV:
            case ACT_DED:
                whoseturn = 1;
            default:
                break;
            }
            p0 += r0.move;
        } else {
            LOG(LOG_INFO, "Program 1's turn\n");
            r1 = op(registers1, instructions, ninst, p1, signals1);
            switch (r1.action) {
            case ACT_SND:
                Queue_append(signals0, r1.val);
                part2++;
                break;
            case ACT_RCV:
            case ACT_DED:
                whoseturn = 0;
            default:
                break;
            }
            p1 += r1.move;
        }
    }
    printf("Part 2: %zu\n", part2);
    return 0;
}
