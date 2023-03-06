struct inner {
  double d;
  char c;
};

struct middle {

  struct inner inner_member;
  struct middle *self_ptr;
};

struct outer {
  struct middle *middle_ptr;
  struct middle middle_member;
};

int main() {
  static struct inner i = {5e41, 'x'};

  struct middle m = {i, &m};
  struct outer o = {&m, m};

  // o.middle_ptr is address of m, so &o.middle_ptr->self_ptr is address of
  // second member of m
  if ((char *)&o.middle_ptr->self_ptr != ((char *)&m + sizeof(struct inner)))
    return 1;

  struct middle *mid_ptr = o.middle_ptr;

  // mid_ptr points to m; m->inner_member.c is second scalar in m
  // right after double  'd' in nested struct
  if ((char *)&mid_ptr->inner_member.c != ((char *)&m + sizeof(double)))
    return 2;

  if ((char *)&mid_ptr->self_ptr->self_ptr !=
      ((char *)&m + sizeof(struct inner)))
    return 3;

  return 0;
}
