int foo = 0;

void set_foo(int a) { foo = a; }

int main() {
  set_foo(12);
  return foo;
}