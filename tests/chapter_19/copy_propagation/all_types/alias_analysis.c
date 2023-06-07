void callee(int *ptr) { *ptr = -1; }

int target(void) {
  int i = 10;
  int j = 20;
  callee(&i);
  i = 4;

  // look for movl $24, %eax (w/ constant fold enabled)
  // can propagate i b/c there are no stores
  // or function calls after i = 4
  // can propagate j b/c it's not aliased
  return i + j;
}

int main(void) { return target(); }