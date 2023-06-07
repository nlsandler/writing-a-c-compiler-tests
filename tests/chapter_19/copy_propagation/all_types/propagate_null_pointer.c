int *target(void) {
  int *ptr = 0;
  int *ptr2 = ptr;
  return ptr2;
}

int main(void) {
  int *result = target();
  return (!result);
}