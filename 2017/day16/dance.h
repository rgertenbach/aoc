#ifndef DANCE_H
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N_PROG 16
// #define N_PROG 5

enum Kind {
    KIND_SPIN = 1,
    KIND_EXCHANGE = 2,
    KIND_PARTNER = 3,
    KIND_DONE = 4
};

struct Exchange {
    size_t a;
    size_t b;
};

struct Partner {
    uint8_t a;
    uint8_t b;
};

struct Instruction {
    enum Kind kind;
    union {
        size_t amount;
        struct Exchange exchange;
        struct Partner partner;
    } args;
};

struct Instruction
parse(FILE * f)
{
    struct Instruction instruction;
    switch (fgetc(f)) {
    case 's':
        instruction.kind = KIND_SPIN;
        fscanf(f, "%zu", &instruction.args.amount);
        break;
    case 'x':
        instruction.kind = KIND_EXCHANGE;
        fscanf(
            f, "%zu/%zu", &instruction.args.exchange.a,
            &instruction.args.exchange.b
        );
        break;
    case 'p':
        instruction.kind = KIND_PARTNER;
        fscanf(
            f, "%c/%c", &instruction.args.partner.a,
            &instruction.args.partner.b
        );
        break;
    case ',':
        instruction = parse(f);
        break;
    default:
        instruction.kind = KIND_DONE;
    }
    return instruction;
}

void
spin(uint8_t progs[], uint8_t const amount)
{
    uint8_t t[N_PROG];
    memcpy(t, progs, N_PROG * sizeof(*progs));
    for (size_t i = 0; i < N_PROG; ++i) {
        progs[(i + amount) % N_PROG] = t[i];
    }
}

void
exchange(uint8_t progs[], struct Exchange e)
{
    uint8_t t;
    t = progs[e.a];
    progs[e.a] = progs[e.b];
    progs[e.b] = t;
}

void
partner(uint8_t progs[], struct Partner p)
{
    uint8_t t;
    size_t a = 100, b = 100;
    for (size_t i = 0; i < N_PROG; ++i) {
        if (progs[i] == p.a) {
            a = i;
        }
        if (progs[i] == p.b) {
            b = i;
        }
    }
    t = progs[a];
    progs[a] = progs[b];
    progs[b] = t;
}

void
process_single_instruction(uint8_t programs[], struct Instruction instruction)
{

    switch (instruction.kind) {
    case KIND_SPIN:
        spin(programs, instruction.args.amount);
        break;
    case KIND_EXCHANGE:
        exchange(programs, instruction.args.exchange);
        break;
    case KIND_PARTNER:
        partner(programs, instruction.args.partner);
        break;
    default:
        break;
    }
}

void
process_instructions(
    uint8_t programs[], struct Instruction * instructions, size_t const ninst
)
{
    for (size_t i = 0; i < ninst; ++i) {
        process_single_instruction(programs, instructions[i]);
    }
}

void
print_progs(uint8_t programs[])
{
    for (size_t i = 0; i < N_PROG; ++i) {
        printf("%c", programs[i]);
    }
    printf("\n");
}

#define DANCE_H
#endif  // DANCE_H
