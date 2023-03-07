struct s;

extern struct s *ptr;

int main() {
  // can't perform pointer addition w/ pointers to incomplete types
  return ptr + 0 == ptr;
}