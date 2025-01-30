#include <limits.h>
#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MAXLEN 10000
#define MAXNUMS 100
#define max(a, b) (((a) > (b)) ? (a) : (b))
#define min(a, b) (((a) < (b)) ? (a) : (b))

int
foo(char const * const s)
{
  int * numbers = malloc(MAXNUMS * sizeof(int));
  size_t n = 0;
  for (size_t i = 0; s[i] != '\0'; ++i) {
    int current = 0;
    while (isdigit(s[i])) {
      current *= 10;
      current += s[i++] - '0';
    }

    for (size_t k = 0; k < n; ++k) {
      int a = max(current, numbers[k]);
      int b = min(current, numbers[k]);
      if (a % b == 0) {
        return a / b;
      }
    }
    numbers[n++] = current;
  }
  return -1;
}

int
main(int const argc, char const * const * const argv)
{
    if (argc < 2) {
        fprintf(stderr, "No input filename provided\n");
        return 1;
    }
    FILE * file = fopen(argv[1], "r");
    if (file == NULL) {
        fprintf(stderr, "Could not open file.\n");
        return 2;
    }
    char * s = malloc(MAXLEN);
    char c;
    int total = 0;
    while ((c = fgetc(file)) != EOF) {
        ungetc(c, file);
        fgets(s, MAXLEN, file);
        total += foo(s);
    }
    fclose(file);
    printf("%d\n", total);
    return 0;
}
