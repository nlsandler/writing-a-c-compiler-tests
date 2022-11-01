int callee(int i) { return i == 4; }

int target() {
  int y = 3;
  int x;
  do {
    x = callee(y);
    y = 4;
  } while (x);
  return y; // should become return 4
}

int main() { return target(); }