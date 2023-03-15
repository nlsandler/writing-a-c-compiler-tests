int strcmp(char *s1, char *s2);
int strncmp(char *s1, char *s2, unsigned long n);

struct one_int {
  int i;
  char c;
};

struct one_int_exactly {
  unsigned long l;
};

struct two_ints {
  char c;
  int arr[3];
};

struct two_ints_nested {
  struct one_int a;
  struct one_int b;
};

struct twelve_bytes {
  int i;
  char arr[8];
};

struct one_xmm {
  double d;
};

struct two_xmm {
  double d[2];
};

struct int_and_xmm {
  char c;
  double d;
};

struct xmm_and_int {
  struct one_xmm dbl;
  char c[3];
};

struct odd_size {
  char arr[5];
};

struct memory {
  double d;
  char c[3];
  long l;
  int i;
};

// passing structures as parameters

// all arguments fit in registers
int pass_small_structs(struct two_xmm two_xmm_struct, struct one_int int_struct,
                       struct one_xmm xmm_struct,
                       struct xmm_and_int mixed_struct,
                       struct twelve_bytes int_struct_2,
                       struct one_int_exactly another_int_struct);

// use remaining structure types, mix with scalars
int structs_and_scalars(long l, double d, struct odd_size os, struct memory mem,
                        struct one_xmm xmm_struct);

// pass a structure in memory b/c we're out of registers
int struct_in_mem(double a, double b, double c, struct xmm_and_int first_struct,
                  double d, struct two_xmm second_struct, long l,
                  struct int_and_xmm third_struct,
                  struct one_xmm fourth_struct);
// pass two_ints_nested in memory b/c can't fit both eightbytes in quadword
int pass_borderline_struct_in_memory(struct two_ints t_i, char c,
                                     struct int_and_xmm i_x, void *ptr,
                                     struct two_ints_nested t_i_n, double d);

// returning structures

struct one_int return_int_struct(void);
struct twelve_bytes return_two_int_struct(void);
struct one_xmm return_double_struct(void);
struct two_xmm return_two_double_struct(void);
struct xmm_and_int return_mixed(void);
struct int_and_xmm return_mixed2(void);
struct memory return_on_stack(void);

// return on stack + pass other int params
struct memory pass_and_return_regs(int i, double d, struct int_and_xmm strct,
                                   char c, struct two_ints t_i, long l,
                                   struct one_int_exactly o_i_e, char c2);