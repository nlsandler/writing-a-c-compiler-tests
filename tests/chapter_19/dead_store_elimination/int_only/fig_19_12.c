int callee(void) { return 4; }

int callee2(void) { return 5; }

int target(int flag) {
  int x = 10; // eliminate this!
  if (flag) {
    x = callee();
  } else {
    x = callee2();
  }
  return x;
}

int main(void) { return target(0) + target(1); }