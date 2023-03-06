struct inner {
  double d;
  char c;
};

struct middle {
  char c;
  struct inner inner_member;
};

struct outer {

  struct middle middle_member;
  struct middle *middle_ptr;
};

int validate(struct outer *outer_ptr);
void *malloc(unsigned long size);