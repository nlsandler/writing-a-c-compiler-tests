int callee() { return 3; }

int target() {
  int x = 2;
  x = callee();
  x = 2;
  return x; // look for movl $2, %eax
}

int main() { return target(); }