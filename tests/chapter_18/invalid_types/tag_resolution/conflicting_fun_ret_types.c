struct s;

struct s foo(void);

int main(void) {
  struct s;
  struct s foo(void); // conflict w/ earlier def; wrong return type
  return 0;
}