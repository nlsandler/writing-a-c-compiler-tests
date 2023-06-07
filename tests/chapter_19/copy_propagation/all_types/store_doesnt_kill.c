int callee(int *p1, int *p2) { return p1 == p2; }

int target(void) {
  int i = 0;
  int *ptr = &i;
  int *ptr2 = ptr; // generate copy ptr2 = ptr
  *ptr = 10;       // this does NOT kill copy
  // make sure both args have same value, since we can replace ptr2 with ptr
  return callee(ptr, ptr2);
}

int main(void) { return target(); }