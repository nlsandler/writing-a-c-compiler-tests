struct s;
int main() {
  struct s {
    int a;
  };
  int count = 0;
  // make sure we can handle struct declarations in for loop headers
  for (struct s init = {10}; init.a > 0; init.a = init.a - 1) {
    count = count + 1;
  }
  return count;
}