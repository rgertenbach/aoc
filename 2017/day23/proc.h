#ifndef PROC_H
#define PROC_H

#include <inttypes.h>
#include <stdbool.h>
#include <stddef.h>

#define PROC_REGISTER_SZ 8

enum OpCode {
    OP_SET = 1,  // x = y
    OP_SUB,      // x -= y
    OP_MUL,      // x += y
    OP_JNZ,      // Jump y if x > 0.
};

enum ArgumentType {
    ARG_NIL = 0,  // Ignore the arg.
    ARG_REG = 1,  // Argument is a register reference.
    ARG_LIT = 2,  // Argument is a literal.
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
    bool mul;
};

struct Instruction parse(char const * s);
int64_t get_value(int64_t const * const registers, struct Argument arg);
struct Result op(int64_t * const registers, struct Instruction const inst);
void print_state(size_t p, int64_t * const registers);

#endif  // PROC_H
