int main() {
  struct s {
    int a;
    int b;
  };
  struct s x; // x is an eight-byte struct
  {
    struct s {
      char arr[15];
    }; // declare a 15-byte struct type
    // in this scope, 'x' has outer type but specifier refers to inner type
    return (sizeof x == 8 && sizeof(struct s) == 15);
  }
}