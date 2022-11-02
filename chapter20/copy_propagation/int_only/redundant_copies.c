int callee() { return 3; }

int target(int flag) {
  int y = callee();
  int x = y;

  // make sure we optimize out jump/label here b/c y = x is redundnat
  if (flag) {
    y = x;
  }
  return y;
}

int main() { return target(0); }