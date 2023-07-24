#include "pass_wonky_struct.h"
void exit(int status);

// make sure we can successfully pass and return structures on the stack
// whose size is not exactly divisible by 8
// (e.g. returning won't clobber neighboring stack values)

struct wonky change_struct(struct wonky arg) {
  char *arr = arg.arr;
  // first make sure it's all zero
  for (int i = 0; i < 19; i = i + 1) {
    if (arr[i]) {
      exit(2);
    }
  }
  arr[0] = 1;
  arr[6] = 6;
  arr[17] = -1;
  return arg;
}