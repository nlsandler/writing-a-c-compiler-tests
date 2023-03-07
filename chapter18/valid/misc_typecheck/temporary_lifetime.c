// a non-lvalue structure that contains an array
// has temporary lifetime;
// you can get the array's address implicitly (but not explicitly)
// NB modifying an array w/ temporary lifetime is undefined

struct inner {
  int a;
  int b;
};

struct contains_array {
  struct inner array[4];
};

struct contains_array get_struct() {
  struct inner obj = {1, 2};
  struct inner obj2 = {3, 4};
  struct contains_array result = {{obj, obj2, obj}};
  return result;
}

int main() {
  int i = get_struct().array[2].a;
  return i;
}