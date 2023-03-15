struct s;
int foo(struct s x);

int main(void) {
  struct s;
  int foo(struct s x); // conflicts w/ earlier declaration, different param type
  return 0;
}