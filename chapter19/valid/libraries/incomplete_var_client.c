struct s;
struct s *get_struct_pointer();
int use_struct_pointer(struct s *ptr);
extern struct s incomplete_var;

int main() {
  struct s *ptr = get_struct_pointer();
  if (&*ptr != ptr)
    return 0;
  return use_struct_pointer(&incomplete_var);
}