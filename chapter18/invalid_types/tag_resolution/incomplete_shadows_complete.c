struct s {
  int a;
};

int main() {
  struct s; // incomplete declaration shadows complete
  struct s *x;
  x->a = 10; // illegal; x has incomplete type w/out member 'a'
  return 0;
}