#include "nested_pointer_access.h"

int main() {
  struct outer *o = malloc(sizeof(struct outer));
  o->middle_ptr = malloc(sizeof(struct middle));
  o->middle_ptr->c = 99;
  struct inner inner = {77.0, 11};
  o->middle_ptr->inner_member = inner;
  o->middle_member.inner_member.c = 0;
  o->middle_member.inner_member.d = 0;

  return validate(o);
}