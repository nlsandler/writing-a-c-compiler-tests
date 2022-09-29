#include "initializers.h"

struct inner basic = {1.0, "hi", {9, 8, 7}};
struct inner partial_init = {2.0, "bye"};

struct outer complex_partial_init = {
    0, 100000l, {{98.0}, {100.0, "nested_string", "ab"}}};

int validate_partial_auto(struct inner *partial) {
  if (partial->d != 55.55 || partial->str || partial->arr[0] ||
      partial->arr[1] || partial->arr[2])
    return 1;
  // we succeeded!
  return 0;
}

int validate_non_static(struct inner *basic_auto, struct inner *basic_auto2,
                        struct outer *complex_auto) {
  // validate first param
  if (basic_auto->d != -55.55 || strcmp(basic_auto->str, "foo") ||
      basic_auto->arr[0] != 'x' || basic_auto->arr[1] != 'y' ||
      basic_auto->arr[2] != 'z')
    return 7;

  // validate second param, should be identical to first
  // str field should have same address, not just same contents
  if (basic_auto2->d != -55.55 || basic_auto->str != basic_auto2->str ||
      basic_auto2->arr[0] != 'x' || basic_auto2->arr[1] != 'y' ||
      basic_auto2->arr[2] != 'z')
    return 8;

  // validate third param
  if (validate_partial_auto(complex_auto->x))
    return 9;

  if (validate_partial_auto(complex_auto->struct_array))
    return 10;

  if (complex_auto->struct_array[1].d || complex_auto->struct_array[1].str ||
      complex_auto->struct_array[1].arr[0] ||
      complex_auto->struct_array[1].arr[1] ||
      complex_auto->struct_array[1].arr[2])
    return 11;

  return 0;
}
