// make sure we copy correct number of bytes when copying sub-object into
// something else

struct inner {
  char char_array[5];
};

struct outer {
  char first;
  char second;
  struct inner nested;
  char last;
};

int main() {
  // this test relies on the fact that we allocate variables contiguously on the
  // stack to validate that copying an aggregate into one object doesn't
  // overwrite the ones next to it. it won't test this anymore once we implement
  // register allocation
  char a = 'a';
  char b = 'b';
  char c = 'c';
  struct inner x = {{0, 0, 0, 0, 0}};
  char d = 'd';
  char e = 'e';
  struct outer y = {-1, -2, {{-3, -4, -5, -6, -7}}, -8};
  x = y.nested;
  char f = 'f';
  char g = 'g';
  if (a != 'a' || b != 'b' || c != 'c' || d != 'd' || e != 'e' || f != 'f' ||
      g != 'g')
    return 1;

  if (x.char_array[0] != -3 || x.char_array[1] != -4 || x.char_array[2] != -5 ||
      x.char_array[3] != -6 || x.char_array[4] != -7)
    return 2;

  return 0;
}