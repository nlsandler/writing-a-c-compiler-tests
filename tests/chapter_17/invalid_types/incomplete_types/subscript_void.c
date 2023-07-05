// you can't subscript pointers to void
// although Clang/GCC allow this as a language extension
int main(void) {
  int x = 10;
  void *v = &x;
  v[0];
  return 0;
}