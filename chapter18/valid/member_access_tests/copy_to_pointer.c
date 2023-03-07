struct inner {
  char a;
  char b;
};

struct middle {
  double d;
  struct inner i;
};

struct outer {
  struct middle m;
  long l;
};

struct outer global_struct = {{1.0, {9, 10}}, 100};

void *malloc(unsigned long size);

int main() {
  struct outer *local_struct = (struct outer *)malloc(sizeof(struct outer));
  *local_struct = global_struct;
  return (local_struct->l == 100 && local_struct->m.d == 1.0 &&
          local_struct->m.i.a == 9 && local_struct->m.i.b == 10);
}