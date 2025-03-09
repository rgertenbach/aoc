#ifndef DUET_H
#define DUET_H

#include <ctype.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <inttypes.h>

#define DUET_REGISTER_SZ 28
#define DUET_LAST_PLAYED 26
#define DUET_RECOVERED 27

enum OpCode {
    // Sounds
    OP_SND = 1,
    // Set register x to value of y
    OP_SET,
    // x += y
    OP_ADD,
    // x *= y
    OP_MUL,
    // x %= y
    OP_MOD,
    // Recover the last played frequency if x is not 0.
    OP_RCV,
    // Jump y if x > 0.
    OP_JGZ,
};

enum ArgumentType {
    // Ignore the arg.
    ARG_NIL = 0,
    // Argument is a register reference.
    ARG_REG = 1,
    // Argument is a literal.
    ARG_LIT = 2,
};

struct Argument {
    enum ArgumentType type;
    int64_t value;
};

struct Instruction {
    enum OpCode op;
    struct Argument x;
    struct Argument y;
};

struct Result {
    ptrdiff_t move;
    bool rec;
};

struct Instruction
parse(char const * s)
{
    struct Instruction inst;
    if (!strncmp(s, "snd", 3)) {
        inst.op = OP_SND;
    } else if (!strncmp(s, "set", 3)) {
        inst.op = OP_SET;
    } else if (!strncmp(s, "add", 3)) {
        inst.op = OP_ADD;
    } else if (!strncmp(s, "mul", 3)) {
        inst.op = OP_MUL;
    } else if (!strncmp(s, "mod", 3)) {
        inst.op = OP_MOD;
    } else if (!strncmp(s, "rcv", 3)) {
        inst.op = OP_RCV;
    } else if (!strncmp(s, "jgz", 3)) {
        inst.op = OP_JGZ;
    }
    s += 4;
    if (isalpha(*s)) {
        inst.x.type = ARG_REG;
        inst.x.value = *(s++) - 'a';
    } else {
        inst.x.type = ARG_LIT;
        sscanf(s, "%ld", &inst.x.value);
        while (*s != ' ' && *s != '\0') {
            s++;
        }
    }
    if (*s != '\0') {
        s++;
    }
    if (*s == '\0') {
        inst.y.type = ARG_NIL;
    } else if (isalpha(*s)) {
        inst.y.type = ARG_REG;
        inst.y.value = *s - 'a';
    } else {
        inst.y.type = ARG_LIT;
        sscanf(s, "%ld", &inst.y.value);
    }
    return inst;
}

int64_t
get_value(int64_t const * const registers, struct Argument arg)
{
    switch (arg.type) {
    case ARG_LIT:
        return arg.value;
    case ARG_REG:
        return registers[arg.value];
    default:
        return 0;
    }
}

struct Result
op(int64_t * const registers, struct Instruction const inst)
{
    struct Result r = { 1, false };
    switch (inst.op) {
    case OP_SND:
        registers[DUET_LAST_PLAYED] = get_value(registers, inst.x);
        break;
    case OP_SET:
        registers[inst.x.value] = get_value(registers, inst.y);
        break;
    case OP_ADD:
        registers[inst.x.value] += get_value(registers, inst.y);
        break;
    case OP_MUL:
        registers[inst.x.value] *= get_value(registers, inst.y);
        break;
    case OP_MOD:
        registers[inst.x.value] %= get_value(registers, inst.y);
        break;
    case OP_RCV:
        if (get_value(registers, inst.x) != 0) {
            registers[DUET_RECOVERED] = registers[DUET_LAST_PLAYED];
            r.rec = true;
        }
        break;
    case OP_JGZ:
        if (get_value(registers, inst.x) > 0) {
            r.move = get_value(registers, inst.y);
        }
    default:
        break;
    }
    return r;
}

#endif  // DUET_H
