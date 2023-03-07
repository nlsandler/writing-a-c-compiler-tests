struct pair {
  int a;
  int b;
};

int main() {
  // not a valid struct initializer
  struct pair x.a = 10;
}