#include "array_of_structs.h"

static struct outer static_array[3] = {
    {0, {0, {0, 0}}}, {2, {3, {4, 5}}}, {4, {6, {8, 10}}}};

int main(void) {
  struct outer auto_array[3] = {
      {0, {0, {0, 0}}}, {2, {3, {4, 5}}}, {4, {6, {8, 10}}}};

  int static_result = validate_struct_array(static_array);
  if (static_result)
    return static_result + 3;
  return validate_struct_array(auto_array);
}