struct s;

extern struct s v;

int main() {
  // incomplete structures can't appear in cast expressions
  (void)v;
  return 0;
}