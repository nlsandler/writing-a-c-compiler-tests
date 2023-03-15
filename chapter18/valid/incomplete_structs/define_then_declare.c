// if we've already defined/declared a struct, declaring it again in the same
// scope does nothing

int main(void) {
  struct s {
    int a;
  };
  struct s; // this does nothing

  struct s x = {1};
  return x.a;
}