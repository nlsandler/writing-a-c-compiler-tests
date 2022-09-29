struct s {
  int i;
};
static struct s internal = {2};

struct s *get_struct_pointer() {
  return &internal;
}

int use_struct_pointer(struct s *ptr) { return ptr->i; }

struct s incomplete_var = {3};
