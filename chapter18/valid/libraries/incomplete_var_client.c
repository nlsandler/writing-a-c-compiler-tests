struct s;
struct s *get_struct_pointer();
int use_struct_pointers(struct s *ptr, struct s *ptr2);
extern struct s incomplete_var;

int main() {
  struct s *ptr = get_struct_pointer();
  return use_struct_pointers(&incomplete_var, ptr);
}