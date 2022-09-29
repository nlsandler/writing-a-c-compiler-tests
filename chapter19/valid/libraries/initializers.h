// test out various forms of iniitalization;
// make sure results are at correct offset

int strcmp(char *s1, char *s2);

struct inner {
  double d;
  char *str;
  char arr[3];
};

struct outer {
  struct inner *x;
  long l;
  struct inner struct_array[2];
};

// static initializers
extern struct inner basic;
extern struct inner partial_init;

extern struct outer complex_partial_init;

int validate_non_static(struct inner *basic_auto, struct inner *basic_auto2,
                        struct outer *complex_auto);
