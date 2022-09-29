// make sure we resolve tags in cast expressions
void *malloc(unsigned long size);
struct s {
  int a;
};

int main() {
  void *ptr = malloc(sizeof(struct s));
  struct s;
  // struct s specifier in cast expression refers to inner, incomplete type
  ((struct s *)ptr)->a = 10;
  return 0;
}