struct s {
  int a;
};

int main() {
  struct s x;
  // we should reject .1l as an invalid preprocessing number,
  // as opposed to accepting it as a dot followed by a valid constant
  return x.1l;
}