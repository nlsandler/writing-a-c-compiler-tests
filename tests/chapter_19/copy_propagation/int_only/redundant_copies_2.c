int callee(void) { return 3; }

int target(int flag, int y) {
  int x = y;

  // make sure we optimize out jump/label here b/c y = x is redundnat
  if (flag) {
    x = y;
  }
  return y;
}

int main(void) { return target(0, 10); }