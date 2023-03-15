struct s;

int main(void) {
  // can't declare a local variable with incomplete struct type
  struct s v;
  return 0;
}