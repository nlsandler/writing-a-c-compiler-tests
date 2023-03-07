int target() {
  // look for: no cmpl, no jne
  return 3 || 99;
}
int main() { return target(); }