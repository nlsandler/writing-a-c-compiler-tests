int target(int flag) {
  int x = 0;
  if (flag) {
    x = 3;
  } else {
    x = 3;
  }
  return x; // look for movl $3, %eax
}

int main() { return target(1) + target(0); }