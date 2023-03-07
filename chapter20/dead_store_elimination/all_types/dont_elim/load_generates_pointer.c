int target() {
  int x = 10;
  int *y = &x;
  return *y; // this uses y, so y = &x isn't a dead store
}

int main() { return target(); }