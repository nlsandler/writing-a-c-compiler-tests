int callee() { return 1 / 0; }

int target() {
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

int main() { return target(); }