#include "param_calling_conventions.h"

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

  // success!
  return 0;
}