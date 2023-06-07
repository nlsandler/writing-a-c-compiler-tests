int callee(void) { return 0; }

int target(void) {
  int x;
  if (0)
    x = callee();
  else
    x = 40;
  return x + 5;
}

int main(void) { return target(); }