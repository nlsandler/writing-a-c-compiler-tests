int *target() {
  int *ptr = 0;
  int *ptr2 = ptr;
  return ptr2;
}

int main() {
  int *result = target();
  return (!result);
}