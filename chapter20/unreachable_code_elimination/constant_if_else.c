int callee() { return 0; }

int target() {
  int x;
  if (0)
    x = callee();
  else
    x = 40;
  return x + 5;
}

int main() { return target(); }