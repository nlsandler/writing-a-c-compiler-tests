int target() {
  int i = 255;
  char c = (char)i;
  i = (int)c;
  return i; // -1
}

int main() { return target() == -1; }