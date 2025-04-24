#include "automaton.h"
#include <stdio.h>
#include <string.h>

struct Replacement
parse_replacement(char const * const s)
{
    struct Replacement repl;
    char match_buf[20], repl_buf[30];
    sscanf(s, "%s => %s", (char *)&match_buf, (char *)&repl_buf);
    if (strlen(match_buf) == 5) {
        repl.match.stride = 2;
        sscanf(
            match_buf, "%2s/%2s", repl.match.pattern, repl.match.pattern + 2
        );
        sscanf(
            repl_buf, "%3s/%3s/%3s", repl.replacement.pattern,
            repl.replacement.pattern + 3, repl.replacement.pattern + 6
        );
    } else {
        sscanf(
            match_buf, "%3s/%3s/%3s", repl.match.pattern,
            repl.match.pattern + 3, repl.match.pattern + 6
        );
        sscanf(
            repl_buf, "%4s/%4s/%4s/%s", repl.replacement.pattern,
            repl.replacement.pattern + 4, repl.replacement.pattern + 8,
            repl.replacement.pattern + 12
        );
        repl.match.stride = 3;
    }
    repl.replacement.stride = repl.match.stride + 1;
    return repl;
}

struct Pattern
pattern_at(
    size_t const row, size_t const col, Grid_t grid, size_t const stride
)
{
    struct Pattern out;
    out.stride = stride;
    size_t n = 0;
    for (size_t ro = 0; ro < stride; ++ro) {
        for (size_t co = 0; co < stride; ++co) {
            out.pattern[n++] = grid[row + ro][col + co];
        }
    }
    return out;
}

struct Pattern
rotate_pattern(struct Pattern p)
{
    struct Pattern out;
    out.stride = p.stride;
    if (p.stride == 2) {
        out.pattern[0] = p.pattern[2];  //  0 1
        out.pattern[1] = p.pattern[0];  //  2 3
        out.pattern[2] = p.pattern[3];
        out.pattern[3] = p.pattern[1];
    } else {
        out.pattern[0] = p.pattern[6];  // 0 1 2
        out.pattern[1] = p.pattern[3];  // 3 4 5
        out.pattern[2] = p.pattern[0];  // 6 7 8
        out.pattern[3] = p.pattern[7];
        out.pattern[4] = p.pattern[4];  // Doesn't move.
        out.pattern[5] = p.pattern[1];
        out.pattern[6] = p.pattern[8];
        out.pattern[7] = p.pattern[5];
        out.pattern[8] = p.pattern[2];
    }
    return out;
}

struct Pattern
hflip_pattern(struct Pattern const p)
{
    struct Pattern out;
    out.stride = p.stride;
    if (p.stride == 2) {
        memcpy(out.pattern + 0, p.pattern + 2, 2);
        memcpy(out.pattern + 2, p.pattern + 0, 2);
    } else {
        memcpy(out.pattern + 0, p.pattern + 6, 3);
        memcpy(out.pattern + 3, p.pattern + 3, 3);
        memcpy(out.pattern + 6, p.pattern + 0, 3);
    }
    return out;
}

struct Pattern
vflip_pattern(struct Pattern const p)
{
    struct Pattern out;
    out.stride = p.stride;
    if (p.stride == 2) {
        out.pattern[0] = p.pattern[1];
        out.pattern[1] = p.pattern[0];
        out.pattern[2] = p.pattern[3];
        out.pattern[3] = p.pattern[2];
    } else {
        out.pattern[0] = p.pattern[2];
        out.pattern[2] = p.pattern[0];
        out.pattern[1] = p.pattern[1];
        out.pattern[3] = p.pattern[5];
        out.pattern[5] = p.pattern[3];
        out.pattern[4] = p.pattern[4];
        out.pattern[6] = p.pattern[8];
        out.pattern[8] = p.pattern[6];
        out.pattern[7] = p.pattern[7];
    }
    return out;
}

static bool
patterns_match_rotation(struct Pattern const p1, struct Pattern const p2)
{
    struct Pattern p = p2;
    if (p1.stride != p2.stride) { return false; }
    for (size_t i = 0; i < 4; ++i) {
        if (!strncmp(p1.pattern, p.pattern, p1.stride * p1.stride)) {
            return true;
        }
        p = rotate_pattern(p);
    }
    return false;
}

bool
patterns_match(struct Pattern const p1, struct Pattern const p2)
{
    struct Pattern p = p1;
    if (p1.stride != p2.stride) { return false; }
    if (patterns_match_rotation(p, p2)) { return true; }
    p = vflip_pattern(p);
    if (patterns_match_rotation(p, p2)) { return true; }
    p = vflip_pattern(p);
    p = hflip_pattern(p);
    if (patterns_match_rotation(p, p2)) { return true; }
    p = vflip_pattern(p);
    if (patterns_match_rotation(p, p2)) { return true; }
    return false;
}

void
insert_pattern(
    Grid_t grid,
    struct Pattern const pattern,
    size_t const row,
    size_t const col
)
{
    switch (pattern.stride) {
    case 2:
        grid[row + 0][col + 0] = pattern.pattern[0];
        grid[row + 0][col + 1] = pattern.pattern[1];
        grid[row + 1][col + 0] = pattern.pattern[2];
        grid[row + 1][col + 1] = pattern.pattern[3];
        break;
    case 3:
        grid[row + 0][col + 0] = pattern.pattern[0];
        grid[row + 0][col + 1] = pattern.pattern[1];
        grid[row + 0][col + 2] = pattern.pattern[2];
        grid[row + 1][col + 0] = pattern.pattern[3];
        grid[row + 1][col + 1] = pattern.pattern[4];
        grid[row + 1][col + 2] = pattern.pattern[5];
        grid[row + 2][col + 0] = pattern.pattern[6];
        grid[row + 2][col + 1] = pattern.pattern[7];
        grid[row + 2][col + 2] = pattern.pattern[8];
        break;
    case 4:
        grid[row + 0][col + 0] = pattern.pattern[0];
        grid[row + 0][col + 1] = pattern.pattern[1];
        grid[row + 0][col + 2] = pattern.pattern[2];
        grid[row + 0][col + 3] = pattern.pattern[3];
        grid[row + 1][col + 0] = pattern.pattern[4];
        grid[row + 1][col + 1] = pattern.pattern[5];
        grid[row + 1][col + 2] = pattern.pattern[6];
        grid[row + 1][col + 3] = pattern.pattern[7];
        grid[row + 2][col + 0] = pattern.pattern[8];
        grid[row + 2][col + 1] = pattern.pattern[9];
        grid[row + 2][col + 2] = pattern.pattern[10];
        grid[row + 2][col + 3] = pattern.pattern[11];
        grid[row + 3][col + 0] = pattern.pattern[12];
        grid[row + 3][col + 1] = pattern.pattern[13];
        grid[row + 3][col + 2] = pattern.pattern[14];
        grid[row + 3][col + 3] = pattern.pattern[15];
        break;
    }
}

struct Pattern
find_replacement(struct Pattern p, struct Replacement * replacements, size_t n)
{
    for (size_t i = 0; i < n; ++i) {
        if (patterns_match(p, replacements[i].match)) {
            return replacements[i].replacement;
        }
    }
    return (struct Pattern){ 0 };
}

size_t
grow(
    Grid_t dest,
    Grid_t grid,
    size_t const n,
    struct Replacement * repls,
    size_t const nrepl
)
{
    size_t stride = (n % 2 == 0) ? 2 : 3;
    size_t segments = n / stride;
    size_t new_stride = stride + 1;
    for (size_t row = 0; row < segments; row++) {
        for (size_t col = 0; col < segments; col++) {
            struct Pattern c =
                pattern_at(row * stride, col * stride, grid, stride);
            struct Pattern new = find_replacement(c, repls, nrepl);
            insert_pattern(dest, new, row * new_stride, col * new_stride);
        }
    }
    return segments * new_stride;
}

void
format_grid(char * dest, Grid_t grid, size_t const n)
{
    size_t const line_length = n + 1;
    for (size_t row = 0; row < n; ++row) {
        size_t row_start = row * line_length;
        memcpy(dest + row_start, grid[row], n);
        dest[row_start + n] = '\n';
    }
    dest[line_length * n - 1] = '\0';
}

size_t
count(Grid_t grid, size_t n)
{
    size_t on = 0;
    for (size_t row = 0; row < n; row++) {
        for (size_t col = 0; col < n; col++) {
            on += grid[row][col] == '#';
        }
    }
    return on;
}

void
format_pattern(char * const dest, struct Pattern const p)
{
    for (size_t row = 0; row < p.stride; ++row) {
        memcpy(
            dest + (row + 1) * (p.stride + 1), p.pattern + row * p.stride,
            p.stride
        );
        dest[(row + 1) * (p.stride + 1)] = '\n';
    }
    dest[(p.stride + 1) * p.stride] = '\n';
}

void
grid_init(Grid_t grid)
{
    char * raw = malloc(GRID_MAX_N * GRID_MAX_N);
    memset(raw, 0, GRID_MAX_N * GRID_MAX_N);
    for (size_t i = 0; i < GRID_MAX_N; ++i) {
        grid[i] = raw + i * GRID_MAX_N;
    }
}

void grid_delete(Grid_t grid)
{
    free(grid[0]);
}

void grid_copy(Grid_t dest, Grid_t source)
{
    memcpy(*dest, *source, SIZEOF_GRID);
}
