int main(void) {
  int arr[3];
  // arr doesn't decay to a pointer here,
  // so the result is 12 (i.e. 3 * 4)
  return sizeof arr;
}