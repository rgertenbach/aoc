#ifndef OP_H
#define OP_H

#include <uthash.h>

#define OP_REG_NAME_MAX_LEN 20

enum Change {
    CHANGE_INC = 1,
    CHANGE_DEC = 2,
};

enum Cmp { CMP_GT = 1, CMP_GE, CMP_LT, CMP_LE, CMP_EQ, CMP_NE };

struct Op {
    char target[OP_REG_NAME_MAX_LEN];
    enum Change change;
    int amt;
    char cond[OP_REG_NAME_MAX_LEN];
    enum Cmp cmp;
    int thresh;
};

struct Op parse(char const * const s);

struct Register {
    char name[OP_REG_NAME_MAX_LEN];
    int value;
    UT_hash_handle hh;
};

struct Register *
get_register(struct Register ** registers, char const * const name);

int set_register(
    struct Register ** registers, char const * const name, int const value
);

int process(struct Register ** registers, struct Op const op);

#endif  // OP_H
