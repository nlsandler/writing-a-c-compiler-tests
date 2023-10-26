#include "missing_retval.h"

#ifdef SUPPRESS_WARNINGS
#pragma GCC diagnostic ignored "-Wreturn-type"
#endif

struct big missing_return_value(int *i) {
    *i = 10;
}