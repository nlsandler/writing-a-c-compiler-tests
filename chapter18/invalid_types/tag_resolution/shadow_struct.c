// Listing 19-30

struct s;
struct s *ptr1 = 0;
int main(void) {
  struct s;
  struct s *ptr2 = 0;
  return ptr1 == ptr2;
}
