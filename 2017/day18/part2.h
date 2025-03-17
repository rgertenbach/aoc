#ifndef DUET_H
#define DUET_H

#include "/home/robin/src/clib/logging/log.h"
#include "queue.h"
#include <ctype.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>

#define DUET_REGISTER_SZ 26

enum Action {
    ACT_NIL = 0,
    ACT_SND = 1,
    ACT_RCV = 2,  // Waiting for a new value
    ACT_DED = 3,
};

enum OpCode {
    // Send register x to queue of other program.
    OP_SND = 1,
    // Set register x to value of y
    OP_SET,
    // x += y
    OP_ADD,
    // x *= y
    OP_MUL,
    // x %= y
    OP_MOD,
    // Receive signal from register
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
    enum Action action;
    int64_t val;  // when action == ACT_SND
};

bool
can_process(struct Result state, struct Queue * signals)
{
    return !(
        (state.action == ACT_RCV && Queue_size(signals) == 0)
        || state.action == ACT_DED
    );
}

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
op(int64_t * const registers,
   struct Instruction const * insts,
   size_t const ninst,
   size_t const p,
   struct Queue * queue)
{
    struct Result r = { .move = 1, .action = ACT_NIL, .val = 0 };
    if (p >= ninst) {
        r.action = ACT_DED;
        return r;
    }
    struct Instruction inst = insts[p];
    switch (inst.op) {
    case OP_SND:
        r.action = ACT_SND;
        r.val = get_value(registers, inst.x);
        LOG(LOG_DEBUG, "  Sending %zu\n", r.val);
        break;
    case OP_SET:
        registers[inst.x.value] = get_value(registers, inst.y);
        LOG(LOG_DEBUG, "  Setting %c to %ld\n", (char)inst.x.value + 'a',
            get_value(registers, inst.y));
        break;
    case OP_ADD:
        registers[inst.x.value] += get_value(registers, inst.y);
        LOG(LOG_DEBUG, "  Adding %ld to %c\n", get_value(registers, inst.y),
            (char)inst.x.value + 'a');
        break;
    case OP_MUL:
        registers[inst.x.value] *= get_value(registers, inst.y);
        LOG(LOG_DEBUG, "  Multiplying %c by %ld\n", (char)inst.x.value + 'a',
            get_value(registers, inst.y));
        break;
    case OP_MOD:
        registers[inst.x.value] %= get_value(registers, inst.y);
        LOG(LOG_DEBUG, "  Moding %c by %ld\n", (char)inst.x.value + 'a',
            get_value(registers, inst.y));
        break;
    case OP_RCV:
        LOG(LOG_DEBUG, "  Receiving from Queue with len %zu into %c\n",
            Queue_size(queue), (char)inst.x.value + 'a');
        if (Queue_size(queue) > 0) {
            registers[inst.x.value] = Queue_popleft(queue);
            LOG(LOG_DEBUG, "    Popped %ld\n", registers[inst.x.value]);
        } else {
            r.action = ACT_RCV;
            r.move = 0;
            LOG(LOG_DEBUG, "    Waiting for signal\n");
        }
        break;
    case OP_JGZ:
        LOG(LOG_DEBUG, "  Jump based on %c\n", (char)inst.x.value + 'a');
        if (get_value(registers, inst.x) > 0) {
            LOG(LOG_DEBUG, "      Jumped\n");
            r.move = get_value(registers, inst.y);
        }
	break;
    default:
	LOG(LOG_FATAL, "Impossible instruction: %d\n", inst.op);
	exit(5);
        break;
    }
    return r;
}

#endif  // DUET_H
