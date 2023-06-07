extern void *x;

void foo(void) { return; }

int main(void) {
  // the standard is ambiguous on whether you can dereference void *,
  // but you definitely can't dereference it and then assign to the result
  *x = foo();
  return 0;
}