int target() { return 0; }

int main() {
  // overflow in dead code shouldn't cause error
  return 0 && (2147483647 + 10);
}