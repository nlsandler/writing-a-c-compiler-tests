void *malloc(unsigned long size);

int main() {
  void *buffer = malloc(100);
  // this will be 8 b/c buffer is a pointer
  return sizeof(buffer);
}