int callee(int a, int b) { return a + b; }
int target(int flag) {
  int x;
  int y;
  if (flag) {
    y = 10;
    x = y;
  } else {
    y = 20;
    x = y;
  }
  // x = y reaches here, though with different values of y
  // compare to Figure 20-6
  // should return y (which is rip-relative)
  // one catch - what if they decide to be clever and use movl %eax, _y(%rip)
  // instead? (GCC does) maybe we don't need to worry about that
  return callee(x, y);
}

int main() {
  int result = target(0);

  if (result != 40)
    return 0;

  result = target(1);
  if (result != 20)
    return 0;

  return 1;
}