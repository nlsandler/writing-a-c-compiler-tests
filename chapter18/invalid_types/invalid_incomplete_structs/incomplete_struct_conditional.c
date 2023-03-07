struct s;

extern struct s v1;
extern struct s v2;

int main() {
  // don't use incomplete structure types in conditional expression
  1 ? v1 : v2;
}