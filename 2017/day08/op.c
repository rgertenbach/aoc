#include "op.h"
#include <stdbool.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <uthash.h>

struct Op
parse(const char * const s)
{
    struct Op op;
    char chng[4];
    char cmp[3];
    sscanf(
        s, "%s %s %d if %s %s %d", op.target, chng, &op.amt, op.cond, cmp,
        &op.thresh
    );
    op.change = !strcmp(chng, "inc") ? CHANGE_INC : CHANGE_DEC;
    op.cmp
        = (!strcmp(cmp, ">")    ? CMP_GT
           : !strcmp(cmp, ">=") ? CMP_GE
           : !strcmp(cmp, "<")  ? CMP_LT
           : !strcmp(cmp, "<=") ? CMP_LE
           : !strcmp(cmp, "==") ? CMP_EQ
                                : CMP_NE);
    return op;
}

struct Register *
get_register(struct Register ** registers, char const * const name)
{
    struct Register * r = NULL;
    HASH_FIND_STR(*registers, name, r);
    if (!r) {
        r = malloc(sizeof(struct Register));
        strcpy(r->name, name);
        r->value = 0;
        HASH_ADD_STR(*registers, name, r);
    }
    return r;
}

int
set_register(
    struct Register ** registers, char const * const name, int const change
)
{
    struct Register * r = get_register(registers, name);
    r->value += change;
    return r->value;
}

int
process(struct Register ** registers, struct Op const op)
{
    struct Register * r = get_register(registers, op.cond);
    bool is;
    switch (op.cmp) {
    case CMP_GT:
        is = r->value > op.thresh;
        break;
    case CMP_GE:
        is = r->value >= op.thresh;
        break;
    case CMP_LT:
        is = r->value < op.thresh;
        break;
    case CMP_LE:
        is = r->value <= op.thresh;
        break;
    case CMP_EQ:
        is = r->value == op.thresh;
        break;
    case CMP_NE:
        is = r->value != op.thresh;
        break;
    }
    if (!is) {
        return INT_MIN;
    }
    return set_register(
        registers, op.target, (op.change == CHANGE_INC ? op.amt : -op.amt)
    );
}
