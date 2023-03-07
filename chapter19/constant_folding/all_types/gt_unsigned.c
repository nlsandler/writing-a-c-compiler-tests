int target() {
  // make sure we're using unsigned compare
  return 2147483653u > 10u;
}

int main() { return target(); }