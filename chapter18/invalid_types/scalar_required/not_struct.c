struct s {
  int a;
};

int main(void) {
  struct s x = {1};
  return !x; // can't apply boolean operators to structs
}