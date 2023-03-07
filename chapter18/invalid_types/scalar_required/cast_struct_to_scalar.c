struct s {
  int a;
};

int main() {
  struct s x = {1};
  // can't cast struct to a scalar value
  int y = (int)x;
  return y;
}