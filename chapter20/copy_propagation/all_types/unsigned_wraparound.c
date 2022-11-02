unsigned int target() {
  unsigned int i = 10u - 11u;
  return i % 5u;
}

int main() { return target() == 0u; }