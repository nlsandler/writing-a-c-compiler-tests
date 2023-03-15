int target(void) {
  // look for: no cmpl, no jne
  return 3 || 99;
}
int main(void) { return target(); }