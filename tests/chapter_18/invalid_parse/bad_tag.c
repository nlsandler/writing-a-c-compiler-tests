struct s {
  int y;
};

int main(void) {
  // can't parenthesize type tag
  struct(s) var;

  return 0;
}