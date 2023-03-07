struct s;

struct s f();

int main() {
  f(); // can't call a function with an incomplete return type (besides void)
  return 0;
}