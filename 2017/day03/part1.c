#include <stdio.h>
#include "uthash.h"
#include "grid.h"

#define abs(a) ((a) < 0 ? -(a) : a)

int
main(void)
{
    int min_row = 0;
    int max_row = 0;
    int min_col = 0;
    int max_col = 0;
    struct Point p = {.row = 0, .col = 0};
    int current = 1;
    enum Direction d = D_RIGHT;
    while (current < 289326) {
      if      (p.col > max_col) { max_col = p.col; d = turn(d); }
      else if (p.row < min_row) { min_row = p.row; d = turn(d); }
      else if (p.col < min_col) { min_col = p.col; d = turn(d); }
      else if (p.row > max_row) { max_row = p.row; d = turn(d); }
      p = move(p, d);
      ++current;
    }
    printf("%d\n", abs(p.row) + abs(p.col));
}
