void *malloc(unsigned long size);

int main() {
  void *x = malloc(100);
  x = x + 1;
  return 0;
}