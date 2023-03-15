int callee(int a, int b) { return a + b; }
int f(void) {
  return 3;
}
int target(void) {
  int x = f();
  int y = x;
  // look for: same value passed in ESI, EDI
  // NOTE: this could be accomplished using either copy propagation
  // or copy coalescing in register allocator
  return callee(x, y);
}

int main(void) { return target(); }
