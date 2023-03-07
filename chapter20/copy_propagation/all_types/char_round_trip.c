int target() {
  int i = 257;
  char c = i;
  return (int)c; //
}

int main() { return target() == 1; }