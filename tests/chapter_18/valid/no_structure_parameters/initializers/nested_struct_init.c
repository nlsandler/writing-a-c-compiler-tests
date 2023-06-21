#ifdef SUPPRESS_WARNINGS
#ifdef __clang__
#pragma clang diagnostic ignored "-Wincompatible-library-redeclaration"
#else
#pragma GCC diagnostic ignored "-Wbuiltin-declaration-mismatch"
#endif
#endif

int strcmp(char *s1, char *s2);

/* NOTE not supporting nested struct declarations */
struct inner {
  int x;
  int y;
  char arr[3];
};

struct outer {
  long l1;
  struct inner i;
  long l2;
};

int main(void) {
  struct outer foo = {100, {3, 4, "!?"}, 10000000};
  if (strcmp(foo.i.arr, "!?"))
    return 0;
  return foo.i.x + foo.i.y + foo.l1 + (foo.l2 - 9999950);
}