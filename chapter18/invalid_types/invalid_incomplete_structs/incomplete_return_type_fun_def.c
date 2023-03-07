// can't define a structure with an incomplete return type
struct s return_struct() {

  struct s result = {1, 2};
  return result;
}
struct s {
  int a;
  int b;
};
int main() { return 0; }