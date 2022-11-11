int target(int arg) {
  static int i;
  if (arg < 0)
    return i;
  i = 5; // this is dead
  i = arg;
  return i;
}

int main() {
  int result1 = target(2);
  int result2 = target(-1);
  return result1 == 2 && result2 == 2;
}