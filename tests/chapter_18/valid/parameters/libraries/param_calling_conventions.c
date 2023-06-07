#include "param_calling_conventions.h"

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