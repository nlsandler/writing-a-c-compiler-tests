int target(void) {
  int i = 255;
  char c = (char)i;
  i = (int)c;
  return i; // -1
}

int main(void) { return target() == -1; }