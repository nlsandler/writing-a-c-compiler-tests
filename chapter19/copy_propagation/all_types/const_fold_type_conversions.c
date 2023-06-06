// check that we correctly propagate copies into type conversion instructions

int target(void) {
  unsigned char c = 250;
  int i = c * 2;             // 500
  double d = i * 1000.;      // 500000.0
  unsigned long l = d / 6.0; // 83333
  d = l + 5.0;
  return d;
}

int main(void) { return target() == 83338; }