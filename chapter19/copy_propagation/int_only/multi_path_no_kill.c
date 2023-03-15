
int var = 0;
int callee(void) {
  var = var + 1;
  return 0;
}

int target(int flag) {
  int x = 3;
  if (flag)
    callee();
  return x; // look for movl $3, %eax
}

int main(void) {
  int result = target(0);
  result = result + target(1);
  return result == 6 && var == 1;
}