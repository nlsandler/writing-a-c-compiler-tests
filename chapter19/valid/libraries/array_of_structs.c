#include "array_of_structs.h"

int validate_struct_array(struct outer *struct_array) {
  for (int i = 0; i < 3; i = i + 1) {
    if (struct_array[i].a != i * 2)
      return i;
    if (struct_array[i].b.l != i * 3)
      return i * 10;
    if (struct_array[i].b.arr[0] != i * 4)
      return i * 25;
    if (struct_array[i].b.arr[1] != i * 5)
      return i * 11;
  }
  return 0;
}