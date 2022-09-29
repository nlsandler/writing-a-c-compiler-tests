struct s {
  int arr[3];
  double d;
};

int main() {
  struct s x = {{1, 2, 3}, 4.0};
  struct s y = {{9, 8, 7}, 6.0};
  // can't assign to this struct, it's not an lvalue
  (1 ? x : y).d = 0.0;

  return 0;
}