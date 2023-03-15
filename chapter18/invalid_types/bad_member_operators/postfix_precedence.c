int main(void) {
  struct s {
    int a;
  };
  struct s x = {10};
  // postfix operatpors have higher precedence,
  // so this is equivalent to &(x->a),
  // which is invalid b/c x isn't a pointe
  return &x->a;
}