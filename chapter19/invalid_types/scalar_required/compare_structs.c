struct s {
  int a;
};

int main() {
  struct s x = {1};
  struct s y = {2};
  return x == y;
}