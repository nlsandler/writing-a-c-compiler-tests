int callee(void) { return 1; }

int target(void) {

  // make sure there's nothing after ret statement/epilogue
  return 2;
  int x = callee();

  if (x) {
    x = 10;
  }

  int y = callee();
  return x + y;
}

int main(void) { return target(); }