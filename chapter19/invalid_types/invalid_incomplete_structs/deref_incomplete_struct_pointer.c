struct s;

struct s *ptr = 0;

int main() {
  // can't dereference pointer to incomplete type
  // except in expression &*ptr
  *ptr;
  return 0;
}