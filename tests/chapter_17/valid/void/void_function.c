int foo = 0;

void set_foo(int a) { foo = a; }
void do_nothing(void) {;}

int main(void) {
  set_foo(12);
  do_nothing();
  return foo;
}