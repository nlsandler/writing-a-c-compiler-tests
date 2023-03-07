int target(int x, int y) {
  // make sure that having empty blocks after optimization doesn't break
  // anything
  if (x) {
    // empty statement
    if (y) {
    }
  }
  return 1;
}

int main() { return target(1, 1) == 1 && target(0, 0) == 1; }