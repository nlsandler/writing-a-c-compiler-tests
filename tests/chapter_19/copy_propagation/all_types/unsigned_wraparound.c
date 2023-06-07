unsigned int target(void) {
  unsigned int i = 10u - 11u;
  return i % 5u;
}

int main(void) { return target() == 0u; }