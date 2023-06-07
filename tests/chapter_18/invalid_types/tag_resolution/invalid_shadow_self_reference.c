struct s {
  int a;
};

int main(void) {
  struct s {
    // can't do this, because tag 's' refers to the type we're declaring now
    // instead of the type we declared earlier
    struct s nested;
  };
  return 0;
}