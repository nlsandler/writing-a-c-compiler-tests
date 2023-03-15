int foo(void) {
  struct s {
    int a;
    int b;
  };
  struct s result = {1, 2};
  return result.a + result.b;
}

int main(void) {
  // previously define struct s is not visible here,
  // so this is trying to define a variable with incomplete type
  struct s blah = {foo(), foo()};
  return blah.a;
}