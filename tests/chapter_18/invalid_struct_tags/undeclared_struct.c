int main(void) {
  // it's illegal to define a variable with an undeclared tag
  // we'll reject this during tag resolution;
  // most compilers would reject it b/c 'struct s' is incomplete
  struct s var;
  return 0;
}