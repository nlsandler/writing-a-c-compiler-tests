int target() {
  int nested[3][23] = {{0, 1}, {2}};
  // w/ constant folding and copy prop this doesn't require movslq or imul
  // instructions
  return nested[1][0];
}

int main() { return target(); }