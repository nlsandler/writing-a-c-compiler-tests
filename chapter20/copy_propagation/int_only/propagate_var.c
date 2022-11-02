int callee(int a, int b) { return a + b; }

int target() {
  int x = callee(1, 2);
  int y = x;
  // look for: same value passed in ESI, EDI
  // NOTE: this could be accomplished using either copy propagation
  // or copy coalescing in register allocator
  return callee(x, y);
}

int main() { return target(); }
