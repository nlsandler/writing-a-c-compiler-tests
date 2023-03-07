struct one {
  int x;
  int y;
};

struct two {
  int a;
  int b;
};

int main() {
  struct one x = {1, 2};
  struct two y = x; // can't initialize from differnet struct type
  return 0;
}