int x = 0;

int target() {
  // we can propagate value of x, even though it has static storage duration,
  // b/c no intervening reads/writes
  x = 10;
  int y = x;
  return y; // should become "return 10"
}

int main() {
  int result = target();
  return result == 10 && x == 10;
}