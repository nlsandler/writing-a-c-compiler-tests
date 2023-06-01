#include "missing_retval.h"

struct big missing_return_value(int *i) {
  *i = 10;
}