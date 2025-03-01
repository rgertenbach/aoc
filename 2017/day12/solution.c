#include "/home/robin/src/clib/string/split.h"
#include "graph.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <uthash.h>

#define MAXLEN 1000
#define IDLEN 10
#define MAXIDS 100

void
process_line(struct Graph ** graph, char const * const input)
{
    (void)graph;
    char left[MAXLEN];
    char right[MAXLEN];
    char * parts[2];
    parts[0] = left;
    parts[1] = right;
    char id_buffer[MAXLEN];
    char * ids[MAXIDS];
    for (size_t i = 0; i < MAXIDS; ++i) {
        ids[i] = id_buffer + i * IDLEN;
    }
    strsplit(parts, input, " <-> ");
    size_t n_dst = strsplit(ids, right, ", ");
    int32_t src = atoi(left);
    for (size_t i = 0; i < n_dst; ++i) {
        int32_t dst = atoi(ids[i]);
        add_edge(graph, src, dst);
        add_edge(graph, dst, src);
    }
}

struct IntSet {
    int32_t id;
    UT_hash_handle hh;
};

bool
set_has(struct IntSet * set, int32_t const id)
{
    struct IntSet * r = NULL;
    HASH_FIND_INT(set, &id, r);
    return !!r;
}

void
set_add(struct IntSet ** set, int32_t const id)
{
    struct IntSet * x = malloc(sizeof(struct IntSet));
    x->id = id;
    HASH_ADD_INT(*set, id, x);
}

void
set_clear(struct IntSet ** set)
{
    struct IntSet *a, *b;
    HASH_ITER(hh, *set, a, b)
    {
        HASH_DEL(*set, a);
        free(a);
    }
}

size_t
part1(struct Graph * const graph)
{
    struct Graph * node = get_node(graph, 0);
    struct IntSet * visited = NULL;
    set_add(&visited, 0);
    struct Graph * current[MAXIDS] = { node };
    size_t n_current = 1;
    struct Graph * next[MAXIDS] = { node };
    size_t n_next = 0;
    while (n_current) {
        for (size_t i = 0; i < n_current; ++i) {
            node = current[i];
            for (size_t n = 0; n < node->n_neighbors; ++n) {
                struct Graph * neighbor = get_node(graph, node->neighbors[n]);
                if (!set_has(visited, neighbor->node)) {
                    set_add(&visited, neighbor->node);
                    next[n_next++] = neighbor;
                }
            }
        }

        memcpy(current, next, n_next * sizeof(struct Graph *));
        n_current = n_next;
        n_next = 0;
    }
    size_t out = HASH_COUNT(visited);
    set_clear(&visited);
    return out;
}

int
main(int const argc, char const * const * const argv)
{
    if (argc < 2) {
        fprintf(stderr, "Need to supply filename\n");
        exit(1);
    }
    FILE * f = fopen(argv[1], "r");
    if (!f) {
        fprintf(stderr, "Could not open %s\n", argv[1]);
        exit(1);
    }
    char s[MAXLEN];

    struct Graph * graph = NULL;

    while (fgets(s, MAXLEN, f)) {
        s[strlen(s) - 1] = '\0';  // Trim newline.
        process_line(&graph, s);
    }
    fclose(f);
    printf("%zu\n", part1(graph));

    return 0;
}
