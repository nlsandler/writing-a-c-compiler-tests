struct s {
  int a;
};

int main() {
  struct s {
    // can't do this, because tag 's' refers to the type we're declaring now
    // instead of the type we declared earlier
    // (make sure we add new tag to current scope before we process its members)
    struct s nested;
  };
  return 0;
}