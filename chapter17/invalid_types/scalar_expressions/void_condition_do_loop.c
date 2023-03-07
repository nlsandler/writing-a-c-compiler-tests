void f() { return; }
int main() {
  int i = 0;
  do {
    i = i + 1;
  } while (f());
  return 0;
}