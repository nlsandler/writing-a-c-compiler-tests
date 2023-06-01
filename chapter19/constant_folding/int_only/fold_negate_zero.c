int target(void) {
  // look for instruction movl -3, <anything>
  // and no negl instruction
  return -0;
}

int main(void) { return target() == 0; }