struct s;
struct s *get_struct_pointer();
void *malloc(unsigned long size);

int main() {
  struct s *ptr = get_struct_pointer();
  // test that we can dereference an incomplete type and then take its address
  // (GCC fails to compile this before version 10; see https://gcc.gnu.org/bugzilla/show_bug.cgi?id=88827)
  return &*ptr == ptr;
}

struct s *get_struct_pointer() {
    return malloc(8);
}