int target(void) {
  int x = -100;
  int y = x * 3 / 5;
  return (y < 100 ? x % 3 : x / 4);
}

int main(void) { return target() == -1; }