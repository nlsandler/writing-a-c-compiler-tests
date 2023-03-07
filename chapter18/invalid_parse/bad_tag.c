struct s {
  int y;
};

int main() {
  // can't parenthesize type tag
  struct(s) var;

  return 0;
}