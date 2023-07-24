void *malloc(unsigned long size);

struct a {
  int x;
  int y;
};

struct b {
  int m;
  int n;
};

int main(void) {
  struct a *ptr = malloc(sizeof(struct a));
  ptr->m = 10; // wrong member name
  return 0;
}
