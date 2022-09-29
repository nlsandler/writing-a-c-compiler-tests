#include "nested_pointer_access.h"

int validate(struct outer *outer_ptr) {
  if (outer_ptr->middle_ptr->c != 99)
    return 1;
  struct inner i = outer_ptr->middle_ptr->inner_member;
  if (i.c != 11 || i.d != 77.0)
    return 2;

  struct outer outer_val = *outer_ptr;
  // middle_ptr in both structs point to same value
  outer_ptr->middle_ptr->c = 4;
  struct inner i2 = {33.3, 3};
  outer_val.middle_ptr->inner_member = i2;

  if (outer_val.middle_ptr->c != 4)
    return 3;

  if (outer_ptr->middle_ptr->inner_member.d != 33.3)
    return 4;

  if (outer_val.middle_ptr->inner_member.c != 3)
    return 5;

  return 0;
}