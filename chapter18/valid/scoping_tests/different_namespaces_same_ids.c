// variables, structure tags, and struct members are all in different namespaces
// so it's okay for them to have the same IDs

struct x {
  int x;
};

struct x x = {10};

int main(void) { return x.x; }