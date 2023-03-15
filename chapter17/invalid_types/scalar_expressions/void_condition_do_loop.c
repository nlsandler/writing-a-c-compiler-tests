void f(void) { return; }
int main(void) {
  int i = 0;
  do {
    i = i + 1;
  } while (f());
  return 0;
}