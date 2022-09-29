struct inner {
  int x;
  int y;
};

struct outer {
  int a;
  struct inner b;
};

struct outer return_struct() {
  struct outer result = {1, {2, 3}};
  return result;
}

int main() {
  // can't assign to non-lvalue
  return_struct().b.x = 10;
  return 0;
}