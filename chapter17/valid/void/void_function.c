int foo = 0;

void set_foo(int a) { foo = a; }
void do_nothing() {;}

int main() {
  set_foo(12);
  do_nothing();
  return foo;
}