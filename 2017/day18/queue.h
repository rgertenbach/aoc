#ifndef QUEUE_H
#define QUEUE_H

#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>

struct QueueNode {
    int64_t val;
    struct QueueNode * next;
};

struct Queue {
    struct QueueNode * head;
    struct QueueNode * tail;
    size_t sz;
};

struct Queue *
Queue_new(void)
{
    struct Queue * queue = malloc(sizeof(struct Queue));
    queue->sz = 0;
    queue->head = NULL;
    queue->tail = NULL;
    return queue;
}

void
Queue_append(struct Queue * q, int64_t val)
{
    struct QueueNode * node = malloc(sizeof(struct QueueNode));
    node->val = val;
    node->next = NULL;
    struct QueueNode * next = q->tail;
    if (q->head == NULL) {
        q->head = node;
    }
    q->tail = node;
    if (next != NULL) {
        next->next = node;
    }
    q->sz++;
}

size_t
Queue_size(struct Queue const * const q)
{
    return q->sz;
}

int64_t
Queue_peek(struct Queue const * const q)
{
    return q->head->val;
}

int64_t
Queue_popleft(struct Queue * q)
{
    struct QueueNode * node = q->head;
    int64_t out = node->val;
    q->head = node->next;
    if (q->tail == node) {
        q->tail = NULL;
    }
    free(node);
    q->sz--;
    return out;
}

void
Queue_delete(struct Queue * q)
{
    while (Queue_size(q) > 0) {
        Queue_popleft(q);
    }
    free(q);
}

#endif  // QUEUE_H
