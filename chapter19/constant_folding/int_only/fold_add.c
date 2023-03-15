int target(void) {
  // look for movl $300, <something>
  // and no add instruction
  return 100 + 200;
}

int main(void) { return target(); }