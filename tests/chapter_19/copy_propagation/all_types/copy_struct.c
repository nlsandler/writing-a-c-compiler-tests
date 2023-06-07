struct s {
  int x;
  int y;
};

int callee(struct s a, struct s b) { return a.x + b.x; }

int target(void) {
  struct s s1 = {1, 2};
  struct s s2 = {3, 4};
  s1 = s2; // generate s1 = s2

  // pass same value for both arguments
  return callee(s1, s2);
}

int main(void) { return target(); }