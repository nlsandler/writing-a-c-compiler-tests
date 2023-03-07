int callee(int arg) { return arg * 2; }

int target(int arg) {
  int x = arg + 1; // not dead
  int y = callee(x);
  x = 10; // dead
  return y;
}

int main() { return target(4); }