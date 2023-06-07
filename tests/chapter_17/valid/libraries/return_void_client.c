void recursive_decrement(unsigned int *ptr);

int main(void) {
  unsigned int i = 77;
  recursive_decrement(&i);
  return i;
}