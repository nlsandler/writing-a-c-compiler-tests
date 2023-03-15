#include "initializers.h"

char *get_string(void) { return "foo"; }

// validate static/global variables defined in the other file
int validate_static(void) {
  // first validate basic
  if (basic.d != 1.0 || strcmp(basic.str, "hi"))
    return 1;
  if (basic.arr[0] != 9 || basic.arr[1] != 8 || basic.arr[2] != 7)
    return 2;
  // now validate partial_init
  if (partial_init.d != 2.0 || strcmp(partial_init.str, "bye") ||
      // array elements should be 0 b/c not explicitly initialized
      partial_init.arr[0] || partial_init.arr[1] || partial_init.arr[2])
    return 3;

  // validate complex_partial_init
  if (complex_partial_init.x || complex_partial_init.l != 100000l)
    return 4;

  // validate first inner struct
  if (complex_partial_init.struct_array[0].d != 98.0 ||
      complex_partial_init.struct_array[0].str ||
      complex_partial_init.struct_array[0].arr[0] ||
      complex_partial_init.struct_array[0].arr[1] ||
      complex_partial_init.struct_array[0].arr[2])
    return 5;

  // validate second inner struct
  if (complex_partial_init.struct_array[1].d != 100.0 ||
      strcmp(complex_partial_init.struct_array[1].str, "nested_string") ||
      complex_partial_init.struct_array[1].arr[0] != 'a' ||
      complex_partial_init.struct_array[1].arr[1] != 'b' ||
      complex_partial_init.struct_array[1].arr[2])
    return 6;

  // we succeeded!
  return 0;
}

int main(void) {

  int static_result = validate_static();
  if (static_result) {
    return static_result;
  }

  // define some structs with automatic storage duration,
  // then have other translation unit validate them
  // make sure to use non-constant expressions in this
  double x = 55.55;
  struct inner basic_auto = {-x, get_string(), "xyz"};
  struct inner basic_auto_copy = basic_auto;
  double *dbl_ptr = &x;
  struct inner partial_auto = {*dbl_ptr};

  struct outer complex = {&partial_auto, (long)x, {partial_auto}};

  return validate_non_static(&basic_auto, &basic_auto_copy, &complex);
}
