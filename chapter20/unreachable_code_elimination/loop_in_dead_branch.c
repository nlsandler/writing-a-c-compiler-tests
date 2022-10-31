int callee() { return 1 / 0; }

int target() {

  int x = 0;
  if (0) {
    /* make sure we eliminate this loop even though every block in it has a
     * predecessor */
    for (int i = 0; i < 10; i = i + 1) {
      x = x + callee();
    }
  }

  return x;
}

int main() { return target(); }