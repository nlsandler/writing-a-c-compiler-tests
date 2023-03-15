#include "classes.h"

int main(void) {
  struct one_int one_int = {54320, 'c'};
  struct one_int_exactly one_long = {567890l};
  struct two_ints two_ints = {'_', {5, 6, 7}};
  struct two_ints_nested two_ints_nested = {one_int, one_int};
  struct twelve_bytes xii = {123, "string!"};

  struct one_xmm one_xmm = {5.125};
  struct two_xmm two_xmm = {{55.5, 44.4}};
  struct int_and_xmm int_and_xmm = {'p', 4.56};
  struct xmm_and_int xmm_and_int = {{1.234}, "hi"};

  struct odd_size odd = {"lmno"};
  struct memory mem = {15.75, "rs", 4444, 3333};

  int retval;

  // test parameter passing

  retval =
      pass_small_structs(two_xmm, one_int, one_xmm, xmm_and_int, xii, one_long);
  if (retval) {
    return retval;
  }

  retval = structs_and_scalars(10, 10.0, odd, mem, one_xmm);
  if (retval) {
    return retval;
  }

  retval = struct_in_mem(10.0, 11.125, 12.0, xmm_and_int, 13.0, two_xmm, 0,
                         int_and_xmm, one_xmm);
  if (retval)
    return retval;

  retval = pass_borderline_struct_in_memory(two_ints, '!', int_and_xmm, 0,
                                            two_ints_nested, 7.8);
  if (retval)
    return retval;

  // returning structures

  struct one_int s1 = return_int_struct();
  if (s1.i != 1 || s1.c != 2) {
    return 26;
  }

  struct twelve_bytes s2 = return_two_int_struct();
  if (s2.i != 10 || strncmp(s2.arr, "12345678", sizeof s2.arr))
    return 27;

  struct one_xmm s3 = return_double_struct();
  if (s3.d != 100.625)
    return 28;
  struct two_xmm s4 = return_two_double_struct();
  if (s4.d[0] != 8.8 || s4.d[1] != 7.8)
    return 29;

  struct xmm_and_int s5 = return_mixed();
  if (s5.dbl.d != 10.0 || strcmp(s5.c, "ab"))
    return 30;

  struct int_and_xmm s6 = return_mixed2();
  if (s6.c != 127 || s6.d != 34e43)
    return 31;

  struct memory s7 = return_on_stack();
  if (s7.d != 1.25 || strcmp(s7.c, "xy") || s7.l != 100l || s7.i != 44)
    return 32;

  s7 = pass_and_return_regs(6, 4.0, int_and_xmm, 5, two_ints, 77, one_long, 99);
  // something was clobbered or set incorrectly in retval
  if (s7.d || s7.c[0] || s7.c[1] || s7.c[2])
    return 33;

  // i was set to indicate problem w/ parameter passing
  if (s7.i)
    return 100 + s7.i;

  if (s7.l != 100)
    return 34; // l field was clobbered or set incorrectly

  // success!
  return 0;
}