int target() {
  // look for instruction movl -3, <anything>
  // and no negl instruction
  return -3;
}

int main() { return target() == -3; }