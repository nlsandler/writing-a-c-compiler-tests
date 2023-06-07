// cf figure 20-11
int f(int arg, int flag) {
  int x = arg * 2;
  if (flag)
    return x;
  return 0;
}

int main(void) { return f(20, 1) + f(3, 0); }