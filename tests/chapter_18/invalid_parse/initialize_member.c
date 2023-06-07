struct pair {
  int a;
  int b;
};

int main(void) {
  // not a valid struct initializer
  struct pair x.a = 10;
}