#include "proc.h"
#include <ctype.h>
#include <string.h>
#include <stdio.h>

struct Instruction
parse(char const * s)
{
    struct Instruction inst;
    if (!strncmp(s, "set", 3)) {
        inst.op = OP_SET;
    } else if (!strncmp(s, "sub", 3)) {
        inst.op = OP_SUB;
    } else if (!strncmp(s, "mul", 3)) {
        inst.op = OP_MUL;
    } else if (!strncmp(s, "jnz", 3)) {
        inst.op = OP_JNZ;
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
    struct Result r = { .move = 1, .mul = false };
    switch (inst.op) {
    case OP_SET:
        registers[inst.x.value] = get_value(registers, inst.y);
        break;
    case OP_SUB:
        registers[inst.x.value] -= get_value(registers, inst.y);
        break;
    case OP_MUL:
        registers[inst.x.value] *= get_value(registers, inst.y);
        r.mul = true;
        break;
    case OP_JNZ:
        if (get_value(registers, inst.x) != 0) {
            r.move = get_value(registers, inst.y);
        }
    default:
        break;
    }
    return r;
}

void print_state(size_t p, int64_t * const registers) 
{
    printf("p: %zu  ", p);
    // A is unused
    for (unsigned char i = 1; i < PROC_REGISTER_SZ; ++i) {
        printf("%c: %8ld  ", i + 'a', registers[i]);
    }
    printf("\n");
}
