int target(void) {
  double d = 1500.0;
  double d2 = d;
  return (int)d + d2;
}

int main(void) { return target() == 3000; }