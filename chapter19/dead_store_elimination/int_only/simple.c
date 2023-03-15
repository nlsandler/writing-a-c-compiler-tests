int target(void) {
  // make sure we don't use constant 10
  int x = 10;
  return 3;
}

int main(void) { return target(); }