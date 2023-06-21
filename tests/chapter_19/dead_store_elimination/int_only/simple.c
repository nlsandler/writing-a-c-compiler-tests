#if defined SUPPRESS_WARNINGS
#pragma GCC diagnostic ignored "-Wunused-variable"
#endif

int target(void) {
  // make sure we don't use constant 10
  int x = 10;
  return 3;
}

int main(void) { return target(); }