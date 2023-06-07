int main(void) {
  int y;
  void *x = &y;
  void *null = 0;
  return x - null;
}