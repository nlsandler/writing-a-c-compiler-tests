int target(void) {
  // make sure we're using unsigned compare
  return 2147483653u > 10u;
}

int main(void) { return target(); }