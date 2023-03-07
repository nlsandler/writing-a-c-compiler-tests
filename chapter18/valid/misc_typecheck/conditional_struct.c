// can use complete structs in conditional expressions

int flag() {
  static int result = 0;
  int retval = result;
  result = result + 1;
  return retval;
}

int main() {
  struct s {
    int x;
  };
  struct s a = {10};
  struct s b = {11};
  int first = (flag() ? a : b).x;
  int second = (flag() ? a : b).x;
  return (first == 11 && second == 10);
}