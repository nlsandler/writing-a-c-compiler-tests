void exit(int status);
int foo() { exit(10); }

int main() {
  // make sure foo isn't actually called
  return sizeof(foo());
}