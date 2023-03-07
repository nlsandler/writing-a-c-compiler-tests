struct s;

extern struct s *ptr;

int main() {
  // can't perform pointer substraction w/ pointers to incomplete types
  return (ptr - ptr) == 0;
}