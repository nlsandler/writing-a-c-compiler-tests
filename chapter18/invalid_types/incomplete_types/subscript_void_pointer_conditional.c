int main() {
  int arr[3] = {1, 2, 3};
  void *void_ptr = arr;
  int *int_ptr = arr + 1;
  // type error: result of conditional is void *,
  // so we can't subscript it
  return (1 ? int_ptr : void_ptr)[1];
}