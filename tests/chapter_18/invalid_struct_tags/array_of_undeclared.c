int main(void) {
  // can't declare array of undeclared/incomplete struct type
  struct s arr[2];
  return 0;
}