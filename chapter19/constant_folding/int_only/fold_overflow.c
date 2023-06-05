int main(void) {
  // overflow in dead code shouldn't cause error
  return 0 && (2147483647 + 10);
}