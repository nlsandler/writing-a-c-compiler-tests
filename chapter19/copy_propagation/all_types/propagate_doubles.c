int target() {
  double d = 1500.0;
  double d2 = d;
  return (int)d + d2;
}

int main() { return target() == 3000; }