struct s {
  int i;
};
static struct s internal = {2};

struct s *get_struct_pointer() {
  return &internal;
}

int use_struct_pointers(struct s *ptr, struct s *ptr2) { return ptr->i + ptr2->i;}

struct s incomplete_var = {3};
