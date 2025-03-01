#ifndef GRAPH_H
#define GRAPH_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <uthash.h>

struct Graph {
    int32_t node;
    int32_t neighbors[1024];
    size_t n_neighbors;
    UT_hash_handle hh;
};

struct Graph *
get_node(struct Graph * graph, int32_t const id)
{
    struct Graph * node = NULL;
    HASH_FIND_INT(graph, &id, node);
    return node;
}

void
add_edge(struct Graph ** graph, int32_t const src, int32_t const dst)
{
    (void)dst;
    struct Graph * node = get_node(*graph, src);

    if (!node) {
        node = malloc(sizeof(struct Graph));
        node->node = src;
        node->n_neighbors = 0;
        HASH_ADD_INT(*graph, node, node);
    }
    node->neighbors[node->n_neighbors++] = dst;
}

void
cleanup_graph(struct Graph * graph)
{
    struct Graph *current, *next;
    HASH_ITER(hh, graph, current, next) { free(current); }
}

#endif  // GRAPH_H
