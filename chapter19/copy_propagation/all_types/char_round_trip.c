int target(void) {
  int i = 257;
  char c = i;
  return (int)c; //
}

int main(void) { return target() == 1; }