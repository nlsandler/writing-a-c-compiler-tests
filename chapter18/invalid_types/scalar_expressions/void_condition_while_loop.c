void f() { return; }
int main() {
  int i = 0;
  while ((void)10) {
    i = i + 1;
  }
  return 0;
}