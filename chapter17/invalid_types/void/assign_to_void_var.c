extern void v1;

int main() {
  // the standard is ambiguous about whether
  // you can declare void variables
  // but you definitely can't assign to them
  v1 = (void)0;
  return 0;
}