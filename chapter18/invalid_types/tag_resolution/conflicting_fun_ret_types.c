struct s;

struct s foo();

int main() {
  struct s;
  struct s foo(); // conflict w/ earlier def; wrong return type
  return 0;
}