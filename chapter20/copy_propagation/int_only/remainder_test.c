// make sure we get remainder and not modulo
// this is really a constant folding test but we couldn't test it until we had
// copy prop since it requires operations w/ negative numbers

int target() {
  // the remainder of 6 % -5 is 1
  // 1 = 6 - (-5) * (-1)
  // but 6 modulo -5 is -
  // -4 = 6 - (-5) * (-2)
  return 6 % -5;
}

int main() { return target(); }