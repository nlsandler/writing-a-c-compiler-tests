// can't define a structure with an incomplete return type
struct s;
struct s return_struct(void) {

  struct s result = {1, 2};
  return result;
}
struct s {
  int a;
  int b;
};
int main(void) { return 0; }