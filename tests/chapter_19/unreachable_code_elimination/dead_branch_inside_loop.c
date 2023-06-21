#if defined SUPPRESS_WARNINGS
#pragma GCC diagnostic ignored "-Wdiv-by-zero"
#endif

int callee(void) { return 1 / 0; }

int target(void) {
  int result = 105;
  // loop is not optimized away but inner function call is
  for (int i = 0; i < 100; i = i + 1) {
    if (0) {
      return callee();
    }
    result = result - i;
  }
  return result;
}

int main(void) { return target(); }