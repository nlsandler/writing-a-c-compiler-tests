int callee(void) { return 100; }

int target(int a) {
  if (a) {
    return 1;
  } else {
    return 2;
  }

  return callee();
}
int main(void) { return (target(1) == 1 && target(0) == 2); }