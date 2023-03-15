#include "classes.h"

int pass_small_structs(struct two_xmm two_xmm_struct, struct one_int int_struct,
                       struct one_xmm xmm_struct,
                       struct xmm_and_int mixed_struct,
                       struct twelve_bytes int_struct_2,
                       struct one_int_exactly another_int_struct) {
  if (two_xmm_struct.d[0] != 55.5 || two_xmm_struct.d[1] != 44.4)
    return 1;

  if (int_struct.c != 'c' || int_struct.i != 54320)
    return 2;
  if (xmm_struct.d != 5.125)
    return 3;
  if (strcmp(mixed_struct.c, "hi") || mixed_struct.dbl.d != 1.234)
    return 4;
  if (strcmp(int_struct_2.arr, "string!") || int_struct_2.i != 123)
    return 5;

  if (another_int_struct.l != 567890)
    return 6;

  return 0;
}

int structs_and_scalars(long l, double d, struct odd_size os, struct memory mem,
                        struct one_xmm xmm_struct) {
  if (l != 10)
    return 7;
  if (d != 10.0)
    return 8;
  if (strcmp(os.arr, "lmno"))
    return 9;
  if (strcmp(mem.c, "rs") || mem.d != 15.75 || mem.i != 3333 || mem.l != 4444)
    return 10;
  if (xmm_struct.d != 5.125)
    return 11;

  return 0;
}

int struct_in_mem(double a, double b, double c, struct xmm_and_int first_struct,
                  double d, struct two_xmm second_struct, long l,
                  struct int_and_xmm third_struct,
                  struct one_xmm fourth_struct) {
  if (a != 10.0 || b != 11.125 || c != 12.0)
    return 12;
  if (strcmp(first_struct.c, "hi") || first_struct.dbl.d != 1.234)
    return 13;
  if (d != 13.0)
    return 14;
  if (second_struct.d[0] != 55.5 || second_struct.d[1] != 44.4)
    return 15;
  if (l)
    return 16;
  if (third_struct.c != 'p' || third_struct.d != 4.56)
    return 17;
  if (fourth_struct.d != 5.125)
    return 18;

  return 0;
}

int pass_borderline_struct_in_memory(struct two_ints t_i, char c,
                                     struct int_and_xmm i_x, void *ptr,
                                     struct two_ints_nested t_i_n, double d) {
  if (t_i.c != '_' || t_i.arr[0] != 5 || t_i.arr[1] != 6 || t_i.arr[2] != 7)
    return 19;
  if (c != '!')
    return 20;
  if (i_x.c != 'p' || i_x.d != 4.56)
    return 21;

  if (ptr)
    return 22;

  if (t_i_n.a.c != 'c' || t_i_n.a.i != 54320)
    return 23;
  if (t_i_n.b.c != 'c' || t_i_n.b.i != 54320)
    return 24;
  if (d != 7.8)
    return 25;
  return 0;
}

struct one_int return_int_struct(void) {
  struct one_int retval = {1, 2};
  return retval;
}

struct twelve_bytes return_two_int_struct(void) {
  struct twelve_bytes retval = {10, "12345678"};
  return retval;
}

struct one_xmm return_double_struct(void) {
  struct one_xmm retval = {100.625};
  return retval;
}
struct two_xmm return_two_double_struct(void) {
  struct two_xmm retval = {{8.8, 7.8}};
  return retval;
}
struct xmm_and_int return_mixed(void) {
  struct xmm_and_int retval = {{10.0}, "ab"};
  return retval;
}
struct int_and_xmm return_mixed2(void) {
  struct int_and_xmm retval = {127, 34e43};
  return retval;
}
struct memory return_on_stack(void) {
  struct memory retval = {1.25, "xy", 100l, 44};
  return retval;
}

int f(char c, double d) {

  if (c == 'p' && d == 4.56)
    return 0;
  return 1;
}

struct memory pass_and_return_regs(int i, double d, struct int_and_xmm strct,
                                   char c, struct two_ints t_i, long l,
                                   struct one_int_exactly o_i_e, char c2) {
  // include stack variables to make sure they don't overwrite return value
  // pointer or vice versa
  int local1 = i * 2;
  double local2 = d * 2;
  struct memory retval = {0, {0, 0, 0}, 0, 0};

  if (local1 != 12 || local2 != 8.0) {
    retval.i = 1;
    return retval;
  }
  int local3 = f(strct.c, strct.d);
  if (local3) {
    retval.i = 2;
    return retval;
  }
  if (c != 5) {
    retval.i = 3;
    return retval;
  }
  if (t_i.c != '_' || t_i.arr[0] != 5 || t_i.arr[1] != 6 || t_i.arr[2] != 7) {
    retval.i = 4;
    return retval;
  }
  if (l != 77) {
    retval.i = 5;
    return retval;
  }
  if (o_i_e.l != 567890) {
    retval.i = 6;
    return retval;
  }
  if (c2 != 99) {
    retval.i = 7;
    return retval;
  }
  retval.l = 100;
  return retval;
}