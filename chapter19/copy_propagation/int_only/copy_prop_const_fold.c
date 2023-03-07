int target() {
  int x = 3;
  int y = x;
  return x + y; // look for movl $6, %eax
}

int main() { return target(); }