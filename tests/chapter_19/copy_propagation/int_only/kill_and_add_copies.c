static int x = 0; // make x static so it's not impacted by dead store elim

int set_x(void) {
  x = 4;
  return 1;
}

int callee(int a, int b) { return a + b; }

int target(void) {
  set_x();
  int y = x; // gen y = x;
  x = 10;    // kill y = x, gen x = 10
  // make sure we propagate x = 10 but not y = x
  return callee(x, y); // becomes use(10, y)
}

int main(void) { return target(); }