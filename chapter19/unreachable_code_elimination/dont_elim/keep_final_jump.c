int target(int a) {
  // make sure we don't choke on a program where final instruction is a jump
  // note that last instruction will only be a jump on second iteration thru
  // pipeline, after we've removed extra Return
  do {
    a = a - 1;
    if (a)
      return 0;
  } while (1);
}

int main() { return target(10); }