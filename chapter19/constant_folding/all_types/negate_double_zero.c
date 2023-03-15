double target(void) { return -0.0; }

int main(void) {
  // 1/0 is infinity, 1/-0 is negative infinity
  return (1 / target()) < 0.0;
}