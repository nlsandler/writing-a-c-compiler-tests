int callee(int i) { return i + 1; }

int target() {
  int x = 5; // dead
  int y = 3; // not
  do {
    x = y * 2;
    y = y + callee(x);
  } while (y < 20);
  return x + y;
}

int main() { return target(); }