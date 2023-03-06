void x() {
  // a function with a void return type can't return an expression
  return 1;
}

int main() {
  x();
  return 0;
}