int main() {
  int arr[3] = {1, 2, 3};
  void *ptr = (void *)arr;
  return ptr < arr + 1;
}