int target(void) {
  // look for instruction movl -3, <anything>
  // and no negl instruction
  return -3;
}

int main(void) { return target() == -3; }