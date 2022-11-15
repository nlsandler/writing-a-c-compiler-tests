// aliased non-static variables are live just after function calls
// but dead at function exit

int b = 0;

void callee(int *ptr) {
  b = *ptr;
  *ptr = 100;
}

int target() {
  int x = 10;
  callee(&x); // uses x
  int y = x;
  x = 50; // this is dead
  return y;
}

int main() {
  int a = target();
  return a == 100 && b == 10;
}