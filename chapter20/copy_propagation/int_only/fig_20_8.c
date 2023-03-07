static int is_called;

int callee(int i) {
  is_called = 1;
  return i == 4;
}

int target() {
  int y = 3;
  int x;
  do {
    x = callee(y);
    y = 4;
  } while (x);
  return y; // should become return 4
}

int main() {
  int result = target();
  return result == 4 && is_called;
}